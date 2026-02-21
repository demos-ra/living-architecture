#!/usr/bin/env node
/**
 * installer-io.js - R4 Execution
 * File system I/O for project scaffolding.
 */

const fs   = require('fs');
const path = require('path');

function copyDir(src, dest) {
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
        const srcPath  = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

function writeFile(filePath, content) {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, content);
}

function exists(filePath) {
    return fs.existsSync(filePath);
}

function chmodExec(filePath) {
    fs.chmodSync(filePath, '755');
}

module.exports = { copyDir, writeFile, exists, chmodExec };
