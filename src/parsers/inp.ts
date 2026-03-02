/**
 * GAMESS Input File Parser
 * Parses GAMESS (US) input files for LSP features
 */

export interface ControlGroup {
  scftyp?: string;
  runtyp?: string;
}

export interface BasisGroup {
  gbasis?: string;
  ngauss?: number;
}

export interface Atom {
  symbol: string;
  atomicNumber: number;
  x: number;
  y: number;
  z: number;
}

export interface DataGroup {
  title?: string;
  symmetry?: string;
  atoms: Atom[];
}

export interface GamessInput {
  contrl?: ControlGroup;
  basis?: BasisGroup;
  data?: DataGroup;
}

/**
 * Parse a line into key-value pairs for GAMESS input format
 */
function parseKeyValueLine(line: string): Record<string, string> {
  const pairs: Record<string, string> = {};
  // Match patterns like "SCFTYP=RHF RUNTYP=OPTIMIZE"
  const regex = /(\w+)\s*=\s*([^\s]+)/g;
  let match;
  while ((match = regex.exec(line)) !== null) {
    pairs[match[1].toUpperCase()] = match[2];
  }
  return pairs;
}

/**
 * Parse $CONTRL group
 */
function parseContrlGroup(content: string): ControlGroup {
  const pairs = parseKeyValueLine(content);
  return {
    scftyp: pairs['SCFTYP'],
    runtyp: pairs['RUNTYP'],
  };
}

/**
 * Parse $BASIS group
 */
function parseBasisGroup(content: string): BasisGroup {
  const pairs = parseKeyValueLine(content);
  return {
    gbasis: pairs['GBASIS'],
    ngauss: pairs['NGAUSS'] ? parseInt(pairs['NGAUSS'], 10) : undefined,
  };
}

/**
 * Parse atom line in $DATA group
 * Format: AtomName AtomicNumber X Y Z
 */
function parseAtomLine(line: string): Atom | null {
  const parts = line.trim().split(/\s+/);
  if (parts.length < 5) {
    return null;
  }
  
  const atomicNumber = parseInt(parts[1], 10);
  if (isNaN(atomicNumber)) {
    return null;
  }
  
  const x = parseFloat(parts[2]);
  const y = parseFloat(parts[3]);
  const z = parseFloat(parts[4]);
  
  if (isNaN(x) || isNaN(y) || isNaN(z)) {
    return null;
  }
  
  return {
    symbol: parts[0],
    atomicNumber,
    x,
    y,
    z,
  };
}

/**
 * Parse $DATA group
 */
function parseDataGroup(content: string): DataGroup {
  const lines = content.split('\n').map(l => l.trim()).filter(l => l.length > 0);
  
  const data: DataGroup = {
    atoms: [],
  };
  
  if (lines.length === 0) {
    return data;
  }
  
  // First line is title
  data.title = lines[0];
  
  // Second line is symmetry (if exists)
  if (lines.length > 1) {
    const symmetryLine = lines[1].toUpperCase();
    if (symmetryLine === 'C1' || symmetryLine.startsWith('CN') || 
        symmetryLine.startsWith('DN') || symmetryLine === 'CS' || 
        symmetryLine === 'CI' || symmetryLine.startsWith('T') || 
        symmetryLine.startsWith('O')) {
      data.symmetry = symmetryLine;
    }
  }
  
  // Remaining lines are atoms
  const startIndex = data.symmetry ? 2 : 1;
  for (let i = startIndex; i < lines.length; i++) {
    const atom = parseAtomLine(lines[i]);
    if (atom) {
      data.atoms.push(atom);
    }
  }
  
  return data;
}

/**
 * Extract content between $GROUP and $END
 */
function extractGroup(input: string, groupName: string): string | null {
  const regex = new RegExp(`\\$${groupName}\\b([^$]*?)\\$END`, 'i');
  const match = input.match(regex);
  return match ? match[1].trim() : null;
}

/**
 * Parse a GAMESS input file
 */
export function parseGamessInput(input: string): GamessInput {
  const result: GamessInput = {};
  
  // Parse $CONTRL group
  const contrlContent = extractGroup(input, 'CONTRL');
  if (contrlContent) {
    result.contrl = parseContrlGroup(contrlContent);
  }
  
  // Parse $BASIS group
  const basisContent = extractGroup(input, 'BASIS');
  if (basisContent) {
    result.basis = parseBasisGroup(basisContent);
  }
  
  // Parse $DATA group
  const dataContent = extractGroup(input, 'DATA');
  if (dataContent) {
    result.data = parseDataGroup(dataContent);
  }
  
  return result;
}

/**
 * Validate GAMESS input file
 */
export function validateGamessInput(input: string): string[] {
  const errors: string[] = [];
  
  if (!input.includes('$CONTRL')) {
    errors.push('Missing required $CONTRL group');
  }
  if (!input.includes('$DATA')) {
    errors.push('Missing required $DATA group');
  }
  
  const parsed = parseGamessInput(input);
  
  if (parsed.contrl && !parsed.contrl.scftyp) {
    errors.push('SCFTYP not specified in $CONTRL group');
  }
  
  if (parsed.data && parsed.data.atoms.length === 0) {
    errors.push('No atoms found in $DATA group');
  }
  
  return errors;
}

export default parseGamessInput;
