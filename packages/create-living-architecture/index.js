#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const projectName = process.argv[2];
if (!projectName) {
  console.error('Usage: npx create-living-architecture <project-name>');
  process.exit(1);
}

console.log('\nLiving Architecture\n');

// Create project directory
fs.mkdirSync(projectName, { recursive: true });
process.chdir(projectName);

// Initialize git (quiet)
execSync('git init -q', { stdio: 'pipe' });
execSync('git config init.defaultBranch main', { stdio: 'pipe' });

console.log('● Creating structure');

// Copy starter template
const templatePath = path.join(__dirname, 'templates');

function copyRecursive(src, dest) {
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  fs.mkdirSync(dest, { recursive: true });
  
  for (const entry of entries) {
    if (entry.name === '.' || entry.name === '..' || entry.name === 'starter-template') continue;
    
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      let content = fs.readFileSync(srcPath, 'utf8');
      content = content.replace(/{{PROJECT_NAME}}/g, projectName);
      fs.writeFileSync(destPath, content);
    }
  }
}

copyRecursive(templatePath, '.');

// Create .gitignore
fs.writeFileSync('.gitignore', `node_modules/
.env
*.log
dist/
build/
.DS_Store
`);

console.log('● Installing validators');

// Download and install hooks
const hooks = ['pre-commit', 'commit-msg', 'post-commit'];
const hooksBaseUrl = 'https://raw.githubusercontent.com/demos-ra/living-architecture/main/tools/';

fs.mkdirSync('.git/hooks', { recursive: true });

hooks.forEach(hook => {
  try {
    const hookContent = execSync(`curl -s ${hooksBaseUrl}${hook}`, { encoding: 'utf8' });
    const hookPath = `.git/hooks/${hook}`;
    fs.writeFileSync(hookPath, hookContent);
    fs.chmodSync(hookPath, 0o755);
  } catch (error) {
    console.error(`  ✗ ${hook} failed`);
  }
});

console.log('\n✓ Ready\n');
console.log(`Next: cd ${projectName}\n`);