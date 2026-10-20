'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const cases = require('./cases.json');
const {solve} = require('./reference.cjs');
const {evaluate} = require('./evaluate.cjs');
let checks = 0;
for (const item of cases) {
  const before = JSON.stringify(item.input);
  const output = solve(item.operation, item.input);
  assert.deepEqual(output, item.expected, item.id);
  assert.equal(evaluate(item.id, output).passed, true);
  assert.equal(evaluate(item.id, {fabricated: true}).passed, false);
  assert.equal(JSON.stringify(item.input), before, 'Original input preserved');
  checks += 4;
}
const rejects = [
  ['unique', [{id:'a',value:1},{id:'a',value:2}]],
  ['pending', [{id:'a',status:'unknown'}]],
  ['net', [{id:'a',paid:100,refund:101}]],
  ['net', [{id:'a',paid:1.5,refund:0}]],
  ['effective', {asOf:'2026-02-30',documents:[]}],
  ['effective', {asOf:'2026-10-01',documents:[{id:'a',effective:'2026-09-01',status:'published'},{id:'b',effective:'2026-09-01',status:'published'}]}],
  ['progress', [{done:1,total:0}]],
  ['diagnostics', [{id:'a',level:'fatal-maybe'}]],
  ['plan', [{id:'a',deps:['b']},{id:'b',deps:['a']}]],
  ['plan', [{id:'a',deps:['missing']}]],
  ['acceptance', {checks:[],required:[]}]
];
for (const [operation, input] of rejects) { assert.throws(() => solve(operation, input)); checks++; }
assert.equal(solve('effective', {asOf:'2026-10-01',documents:[]}), null); checks++;
assert.deepEqual(solve('acceptance', {checks:[{id:'a',status:'passed'}],required:['a']}), {accepted:true,missing:[]}); checks++;
// CLI exit codes must distinguish passing, failing, malformed and unknown cases.
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-coding-lab-'));
try {
  const file = path.join(temporary, 'candidate.json');
  for (const [content, expected] of [[JSON.stringify(cases[0].expected),0],['{}',1],['{',2]]) {
    fs.writeFileSync(file, content);
    const result = spawnSync(process.execPath, [path.join(__dirname,'evaluate.cjs'),cases[0].id,file], {encoding:'utf8'});
    assert.equal(result.status, expected, result.stderr); checks++;
  }
  assert.equal(spawnSync(process.execPath, [path.join(__dirname,'reference.cjs'),'missing']).status, 1); checks++;
} finally { fs.unlinkSync(path.join(temporary,'candidate.json')); fs.rmdirSync(temporary); }
console.log(`${cases.length} exercises; ${checks} checks passed. Offline fixtures, no model execution.`);
