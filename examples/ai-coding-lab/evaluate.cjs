'use strict';
// Evaluates JSON values only; never imports or executes candidate code.
const fs = require('node:fs');
const {isDeepStrictEqual} = require('node:util');
const cases = require('./cases.json');
function evaluate(id, value) {
  const item = cases.find(row => row.id === id);
  if (!item) throw Error('Unknown case id');
  return {id, passed: isDeepStrictEqual(value, item.expected)};
}
module.exports = {evaluate};
if (require.main === module) {
  try {
    if (!process.argv[3]) throw Error('Usage: node evaluate.cjs <case-id> <candidate.json>');
    const value = JSON.parse(fs.readFileSync(process.argv[3], 'utf8').replace(/^\uFEFF/, ''));
    const result = evaluate(process.argv[2], value);
    console.log(JSON.stringify(result));
    process.exitCode = Number(!result.passed);
  } catch (error) { console.error(error.message); process.exitCode = 2; }
}
