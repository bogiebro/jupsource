def trim:
  sub("\\G\\s+"; ""; "m") | sub("\\s+\\z"; ""; "m"); 

def magic_comment:
  if any(test(";$")) then
    map("\(env.COMMENT) " + .)
  else
    .
  end;

.cells | map(if .cell_type == "code" then
    {wrapit: 0, source: .source | trim | split("\n") | magic_comment | join("\n")}
  else
    {source, wrapit: 1}
  end)
