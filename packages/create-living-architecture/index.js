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

// Initialize git
console.log('Initializing git');
execSync('git init', { stdio: 'inherit' });

// Create folder structure
console.log('\nCreating structure');
const folders = [
  'src/domain',
  'src/database',
  'src/api',
  'src/integrations',
  'tests',
  '.git/hooks'
];

folders.forEach(folder => {
  fs.mkdirSync(folder, { recursive: true });
  console.log(`  ● ${folder.split('/').pop()}`);
});

// Create .gitignore
fs.writeFileSync('.gitignore', `node_modules/
.env
*.log
dist/
build/
.DS_Store
__pycache__/
*.pyc
.pytest_cache/
`);

// Create README
fs.writeFileSync('README.md', `# ${projectName}

Living Architecture project.

## Structure

\`\`\`
src/
  domain/         R1 - Zero dependencies
  database/       R2 - Depends on domain
  api/            R3 - Orchestrates domain + database
  integrations/   R4 - External systems + UI
\`\`\`

## Commit Format

\`\`\`
Layer: Description [R#/C#]
\`\`\`

See [Living Architecture](https://github.com/demos-ra/living-architecture) for details.
`);

// Create layer READMEs
const layerDocs = {
  'src/domain/README.md': `# Domain Layer (R1)

Zero dependencies. Core business logic.

## Rules
Cannot import from: Database (R2), API (R3), Integrations (R4)
`,
  'src/database/README.md': `# Database Layer (R2)

Depends on: Domain (R1)

## Rules
Can import from: R1
Cannot import from: R3, R4
`,
  'src/api/README.md': `# API Layer (R3)

Depends on: Domain (R1), Database (R2)

## Rules
Can import from: R1, R2
Cannot import from: R4
`,
  'src/integrations/README.md': `# Integrations Layer (R4)

Depends on: All layers

## Rules
Can import from: R1, R2, R3
External systems and UI live here
`
};

Object.entries(layerDocs).forEach(([file, content]) => {
  fs.writeFileSync(file, content);
});

// Download and install hooks
console.log('\nInstalling validators');
const hooks = ['pre-commit', 'commit-msg', 'post-commit'];
const hooksBaseUrl = 'https://raw.githubusercontent.com/demos-ra/living-architecture/main/tools/';

hooks.forEach(hook => {
  try {
    const hookContent = execSync(`curl -s ${hooksBaseUrl}${hook}`, { encoding: 'utf8' });
    const hookPath = `.git/hooks/${hook}`;
    fs.writeFileSync(hookPath, hookContent);
    fs.chmodSync(hookPath, 0o755);
    console.log(`  ● ${hook}`);
  } catch (error) {
    console.error(`  Failed to download ${hook}`);
  }
});

console.log('\n✓ Ready\n');
console.log('Commit format: Layer: Description [R#/C#]\n');
