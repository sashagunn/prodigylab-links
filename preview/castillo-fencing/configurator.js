import {company} from './company.js';
export function createBrief(input) {
  const length = Number(input.length), height = Number(input.height), gates = Number(input.gates);
  if (!company.materials.includes(input.material)) throw new Error('Choose a listed material.');
  if (!['New installation','Replacement','Repair'].includes(input.work)) throw new Error('Choose a project type.');
  if (String(input.length).trim() === '' || !Number.isFinite(length) || length < 1 || length > 10000) throw new Error('Enter a length between 1 and 10,000 feet.');
  if (![3,4,5,6,7,8].includes(height)) throw new Error('Choose a height between 3 and 8 feet.');
  if (String(input.gates).trim() === '' || !Number.isInteger(gates) || gates < 0 || gates > 20) throw new Error('Enter a whole number of gates from 0 to 20.');
  return `FENCE PROJECT BRIEF\nArea: ${company.region}\nProject: ${input.work}\nMaterial: ${input.material}\nApproximate fence length: ${length} linear feet\nRequested height: ${height} feet\nGates: ${gates}\n\nPlease confirm measurements, site conditions, material availability, scope and pricing with a qualified contractor.\n\nIndependent Preview Factory demo for ${company.name}. Not affiliated with or endorsed by the business. This is a planning brief, not a quote. Nothing has been sent.`;
}
