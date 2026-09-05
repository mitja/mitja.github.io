-- Companion filter for pandoc-pdf.yaml.
-- Exposes the output file name (from -o) to LaTeX as \pdffilename, used in the footer.
local function latex_escape(s)
  return (s:gsub("[\\{}$&#^_%%~]", {
    ["\\"] = "\\textbackslash{}", ["{"] = "\\{", ["}"] = "\\}", ["$"] = "\\$",
    ["&"] = "\\&", ["#"] = "\\#", ["^"] = "\\^{}", ["_"] = "\\_",
    ["%"] = "\\%", ["~"] = "\\~{}",
  }))
end

function Pandoc(doc)
  if not FORMAT:match("latex") then return nil end
  local out = PANDOC_STATE.output_file
  if not out or out == "" then return nil end
  local name = out:match("([^/\\]+)$") or out
  doc.blocks:insert(1, pandoc.RawBlock("latex",
    "\\renewcommand*{\\pdffilename}{" .. latex_escape(name) .. "}"))
  return doc
end
