/**
 * installer-logic.js - R1 Domain
 * Pure scaffold logic. No I/O. Determines what to create and where.
 */

function validateProjectName(name) {
    if (!name || typeof name !== 'string') {
        return { valid: false, error: 'Project name required' };
    }
    if (!/^[a-z0-9-_]+$/i.test(name)) {
        return { valid: false, error: 'Project name must be alphanumeric (hyphens/underscores allowed)' };
    }
    return { valid: true };
}

function buildScaffoldPlan(projectName, laSourceDir) {
    return {
        projectName,
        targetDir:  projectName,
        laSourceDir,
        hooks: {
            preCommit: {
                src:  `${laSourceDir}/src/contract/hooks/pre-commit`,
                dest: `${projectName}/.git/hooks/pre-commit`
            }
        }
    };
}

module.exports = { validateProjectName, buildScaffoldPlan };
