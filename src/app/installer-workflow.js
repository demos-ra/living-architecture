/**
 * installer-workflow.js - R2 Application
 * Orchestrates: validate -> plan -> scaffold -> hook -> commit.
 */

const path     = require('path');
const { execSync } = require('child_process');
const logic    = require('../domain/installer-logic');
const io       = require('../exec/installer-io');

function run(projectName) {
    // 1. Validate
    const validation = logic.validateProjectName(projectName);
    if (!validation.valid) {
        return { success: false, error: validation.error };
    }

    // 2. Check target doesn't already exist
    if (io.exists(projectName)) {
        return { success: false, error: `Directory '${projectName}' already exists` };
    }

    // 3. Build plan
    const laSourceDir = path.resolve(__dirname, '../..');
    const plan = logic.buildScaffoldPlan(projectName, laSourceDir);

    // 4. Copy LA structure
    io.copyDir(path.join(laSourceDir, 'src'),          path.join(plan.targetDir, 'src'));
    io.copyDir(path.join(laSourceDir, '.living-arch'), path.join(plan.targetDir, '.living-arch'));

    // 5. Init git
    execSync(`git init ${plan.targetDir}`, { stdio: 'pipe' });

    // 6. Hook up pre-commit and commit-msg
    const hooksDir   = path.join(plan.targetDir, 'src/contract/hooks');
    const gitHooksDir = path.join(plan.targetDir, '.git/hooks');

    io.chmodExec(path.join(hooksDir, 'pre-commit'));
    io.chmodExec(path.join(hooksDir, 'commit-msg'));

    const preCommitSrc = path.resolve(path.join(hooksDir, 'pre-commit'));
    const commitMsgSrc = path.resolve(path.join(hooksDir, 'commit-msg'));

    io.writeFile(path.join(gitHooksDir, 'pre-commit'), `#!/bin/bash\n"${preCommitSrc}" "$@"\n`);
    io.writeFile(path.join(gitHooksDir, 'commit-msg'), `#!/bin/bash\n"${commitMsgSrc}" "$@"\n`);
    io.chmodExec(path.join(gitHooksDir, 'pre-commit'));
    io.chmodExec(path.join(gitHooksDir, 'commit-msg'));

    // 7. Initial commit — no F-tag, scaffold is not a feature
    execSync('git add .', { cwd: plan.targetDir, stdio: 'pipe' });
    execSync('git commit --no-verify -m "LA v2.0 scaffold"', { cwd: plan.targetDir, stdio: 'pipe' });

    return { success: true, projectName, targetDir: plan.targetDir };
}

module.exports = { run };
