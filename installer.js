#!/usr/bin/env node
/**
 * installer.js - R3 Contract (npx entry point)
 * 
 * Usage:
 *   npx living-architecture <project-name>
 *   node installer.js <project-name>
 */

const workflow = require('./src/app/installer-workflow');

const WIDTH  = 60;
const BORDER = '═'.repeat(WIDTH);
const CENTER = (s) => s.padStart(Math.floor((WIDTH + s.length) / 2)).padEnd(WIDTH);

const projectName = process.argv[2];

if (!projectName) {
    console.log(`\nUsage: npx living-architecture <project-name>`);
    console.log(`Example: npx living-architecture my-app\n`);
    process.exit(1);
}

console.log(`\n${BORDER}`);
console.log(CENTER('LIVING ARCHITECTURE'));
console.log(`${BORDER}\n`);
console.log(`  Creating project: ${projectName}`);

const result = workflow.run(projectName);

if (!result.success) {
    console.log(`\n  ✗ ${result.error}`);
    console.log(`\n${BORDER}\n`);
    process.exit(1);
}

console.log(`\n  ✓ Project created: ${result.targetDir}/`);
console.log(`  ✓ Git initialized`);
console.log(`  ✓ Hooks installed`);
console.log(`  ✓ Initial commit done`);
console.log(`\n  Ready:  cd ${result.projectName}`);
console.log(`\n${BORDER}\n`);
