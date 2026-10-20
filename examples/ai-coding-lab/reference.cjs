'use strict';
// Deterministic teaching baseline, not a model or autonomous agent.
const fs = require('node:fs');
const {isDeepStrictEqual} = require('node:util');
const cases = require('./cases.json');

function unique(rows) {
  const result = [];
  for (const row of rows) {
    if (!row || typeof row.id !== 'string' || !row.id) throw Error('Invalid id');
    const prior = result.find(item => item.id === row.id);
    if (prior && !isDeepStrictEqual(prior, row)) throw Error('Conflicting duplicate: ' + row.id);
    if (!prior) result.push(row);
  }
  return result;
}
function integer(value) {
  if (!Number.isSafeInteger(value) || value < 0) throw Error('Expected nonnegative safe integer');
  return value;
}
function date(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) throw Error('Expected ISO date');
  const parsed = new Date(value + 'T00:00:00Z');
  if (!Number.isFinite(+parsed) || parsed.toISOString().slice(0, 10) !== value) throw Error('Invalid date');
  return value;
}
function solve(operation, input) {
  switch (operation) {
    case 'unique': return unique(input);
    case 'pending':
      if (input.some(row => !['done', 'todo', 'blocked'].includes(row.status))) throw Error('Unknown task status');
      return unique(input).filter(row => row.status !== 'done');
    case 'net': {
      let netCents = 0;
      const pending = [];
      for (const row of unique(input)) {
        integer(row.refund);
        if (row.paid === null) { pending.push(row.id); continue; }
        const paid = integer(row.paid);
        if (row.refund > paid) throw Error('Refund exceeds payment');
        netCents += paid - row.refund;
        integer(netCents);
      }
      return {netCents, pending};
    }
    case 'effective': {
      date(input.asOf);
      const documents = unique(input.documents);
      for (const doc of documents) {
        date(doc.effective);
        if (!['draft', 'published'].includes(doc.status)) throw Error('Unknown document status');
      }
      const eligible = documents.filter(doc => doc.status === 'published' && doc.effective <= input.asOf)
        .sort((a, b) => b.effective.localeCompare(a.effective));
      if (eligible.length > 1 && eligible[0].effective === eligible[1].effective) throw Error('Ambiguous effective version');
      return eligible[0] || null;
    }
    case 'evidence': {
      const supported = [], unsupported = [];
      input.claims.forEach((claim, index) => {
        const valid = claim.sourceId === input.source.id && Object.hasOwn(input.source, claim.field)
          && isDeepStrictEqual(input.source[claim.field], claim.value);
        (valid ? supported : unsupported).push(index);
      });
      return {supported, unsupported};
    }
    case 'progress': return input.map(row => {
      integer(row.done); integer(row.total);
      if (row.done > row.total) throw Error('Completed exceeds total');
      return row.total === 0 ? 0 : Math.round(row.done / row.total * 100);
    });
    case 'diagnostics': {
      const errors = [], warnings = [];
      for (const row of unique(input)) {
        if (!['info', 'warning', 'error'].includes(row.level)) throw Error('Unknown log level');
        if (row.level === 'error') errors.push(row.id);
        if (row.level === 'warning') warnings.push(row.id);
      }
      return {errors, warnings};
    }
    case 'plan': {
      const rows = unique(input), result = [], visiting = new Set();
      function visit(id) {
        if (visiting.has(id)) throw Error('Dependency cycle');
        if (result.includes(id)) return;
        const row = rows.find(item => item.id === id);
        if (!row || !Array.isArray(row.deps)) throw Error('Unknown dependency');
        visiting.add(id);
        row.deps.forEach(visit);
        visiting.delete(id);
        result.push(id);
      }
      rows.forEach(row => visit(row.id));
      return result;
    }
    case 'acceptance': {
      const checks = unique(input.checks);
      if (checks.some(check => !['passed', 'failed', 'not_run'].includes(check.status))) throw Error('Unknown check status');
      if (!Array.isArray(input.required) || !input.required.length
          || input.required.some(id => typeof id !== 'string' || !id)) throw Error('Required checks must be explicit');
      const missing = [...new Set(input.required)].filter(id => !checks.some(check => check.id === id && check.status === 'passed'));
      return {accepted: !missing.length, missing};
    }
    default: throw Error('Unknown operation');
  }
}
module.exports = {solve};
if (require.main === module) {
  try {
    const selected = cases.find(item => item.id === process.argv[2]);
    if (!selected) throw Error('Usage: node reference.cjs <case-id> [input.json]');
    const input = process.argv[3] ? JSON.parse(fs.readFileSync(process.argv[3], 'utf8')) : selected.input;
    process.stdout.write(JSON.stringify(solve(selected.operation, input), null, 2) + '\n');
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
