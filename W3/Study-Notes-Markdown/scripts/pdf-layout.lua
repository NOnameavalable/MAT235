-- Apply print-only layout and anchor fixes; leave HTML/Markdown rendering alone.
local heading_ids = {
  ["A. Problem Type Teaching-Example Solutions"] = "a-problem-type-teaching-example-solutions",
  ["B. Actual Weekly Questions and Solutions"] = "b-actual-weekly-questions-and-solutions",
  ["C. Textbook Exercises and Solutions"] = "c-textbook-exercises-and-solutions",
  ["D. Original Self-Test Questions"] = "d-original-self-test-questions",
  ["E. Self-Test Answers"] = "e-self-test-answers",
  ["F. Coverage and Unresolved Items"] = "f-coverage-and-unresolved-items",
  ["Section 12.4 — Linear Functions (13 exercises)"] = "section-124--linear-functions-13-exercises",
  ["Section 12.5 — Functions of Three Variables (12 exercises)"] = "section-125--functions-of-three-variables-12-exercises",
}

local compact_contours = {
  ["source-textbook-12-4-ex13.png"] = true,
  ["source-textbook-12-4-ex15.png"] = true,
  ["source-textbook-12-4-ex21.png"] = true,
  ["source-textbook-12-4-ex23.png"] = true,
}

local function tex_image(img)
  local height = "0.36"
  for suffix, _ in pairs(compact_contours) do
    if img.src:match(suffix:gsub("%-", "%%-"):gsub("%.", "%%." ) .. "$") then
      height = "0.28"
      break
    end
  end
  local alt = pandoc.utils.stringify(img.caption):gsub("[{}]", "")
  local latex = string.format(
    "\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.72\\linewidth,height=%s\\textheight,keepaspectratio]{%s}\n\\end{figure}",
    height, img.src)
  return pandoc.RawBlock("latex", latex)
end

function Pandoc(doc)
  if FORMAT ~= "latex" then
    return doc
  end

  local blocks = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" then
      local title = pandoc.utils.stringify(block.content)
      local target_id = heading_ids[title]
      if target_id then
        block.identifier = target_id
      end
      if block.level == 3 and title:match("^Problem Type ") then
        table.insert(blocks, pandoc.RawBlock("latex", "\\Needspace{4\\baselineskip}"))
      end
    elseif block.t == "Figure" and #block.content == 1
      and block.content[1].t == "Plain"
      and #block.content[1].content == 1
      and block.content[1].content[1].t == "Image" then
      table.insert(blocks, tex_image(block.content[1].content[1]))
      goto continue
    elseif (block.t == "Para" or block.t == "Plain")
      and #block.content == 1 and block.content[1].t == "Image" then
      table.insert(blocks, tex_image(block.content[1]))
      goto continue
    end
    table.insert(blocks, block)
    ::continue::
  end
  doc.blocks = blocks
  return doc
end
