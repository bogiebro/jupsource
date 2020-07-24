def clen: env.CLEN | tonumber + 1;

def uncomment($commented):
  if $commented then map(.[clen:]) else . end;

def classify($commented):
  if $commented then
    if any(.[clen:] | test(";$")) then 
      "code"
    else "markdown"
    end
  else "code"
  end;

def trim:
  sub("\\G\\n+"; ""; "m") | sub("\\n+\\z"; ""; "m"); 

{cells: [split("\n\n(?!\\s)"; "m")[] | select(. != "") | trim | split("\n") |
  all(startswith("# ")) as $commented |
  classify($commented) as $ty |
  {cell_type: $ty,
  execution_count: null,
  metadata: {trusted: true},
  outputs: [],
  source: uncomment($commented) | join("\n")}],
  nbformat: 4,
  nbformat_minor: 2} 
