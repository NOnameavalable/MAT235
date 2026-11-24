-- Print-only formatting. The Markdown remains the editable content source.
function Header(el)
  local text = pandoc.utils.stringify(el.content)
  local anchor = pandoc.RawBlock('latex', '\\hypertarget{' .. el.identifier .. '}{}')
  if el.level == 2 and (text:match('^Section ') or text == 'Scope, notation, and method selection') then
    return {pandoc.RawBlock('latex', '\\clearpage'), anchor, el}
  end
  if text == 'Method-Selection Decision Guide' then
    return {pandoc.RawBlock('latex', '\\Needspace{26\\baselineskip}'), anchor, el}
  end
  local lines = el.level == 3 and 10 or 5
  return {pandoc.RawBlock('latex', '\\Needspace{' .. lines .. '\\baselineskip}'), anchor, el}
end

function Para(el)
  if #el.content == 1 and el.content[1].t == 'Image' then
    return {pandoc.RawBlock('latex', '\\begin{center}'), el, pandoc.RawBlock('latex', '\\end{center}')}
  end
  if el.content[1] and el.content[1].t == 'Strong' then
    local label = pandoc.utils.stringify(el.content[1])
    local lines = 4
    if label == 'Answer.' then lines = 2 end
    if label:match('Teaching example') or label == 'Question.' then lines = 7 end
    if label:match('A complete answer') then lines = 5 end
    return {pandoc.RawBlock('latex', '\\Needspace{' .. lines .. '\\baselineskip}'), el}
  end
end

function Image(el)
  el.attributes.width = '85%'
  el.attributes.height = '2.8in'
  return el
end

function Code(el)
  if not (el.text:find('/', 1, true) or el.text:find('.pdf', 1, true)) then return end
  local escaped = {}
  local special = {['\\'] = '\\textbackslash{}', ['{'] = '\\{', ['}'] = '\\}',
    ['#'] = '\\#', ['$'] = '\\$', ['%'] = '\\%', ['&'] = '\\&',
    ['^'] = '\\textasciicircum{}', ['~'] = '\\textasciitilde{}'}
  for c in el.text:gmatch('.') do
    if c == '_' then
      escaped[#escaped + 1] = '\\_\\allowbreak{}'
    elseif c == '/' or c == '.' or c == '-' then
      escaped[#escaped + 1] = c .. '\\allowbreak{}'
    elseif c == ' ' then
      escaped[#escaped + 1] = '\\ \\allowbreak{}'
    else
      escaped[#escaped + 1] = special[c] or c
    end
  end
  return pandoc.RawInline('latex', '\\texttt{' .. table.concat(escaped) .. '}')
end

function HorizontalRule(el)
  -- Headings and paragraph spacing already separate sections. A rule alone can
  -- spill onto an otherwise empty page immediately before a forced section break.
  return {}
end

function Link(el)
  local file, anchor = el.target:match('^([%w%-]+)%.md#(.+)$')
  if file then
    -- Hyperref converts a PDF fragment into a named remote destination itself.
    el.target = file .. '.pdf#' .. anchor
  elseif el.target:match('^[%w%-]+%.md$') then
    el.target = el.target:gsub('%.md$', '.pdf')
  end
  return el
end

function Table(el)
  local widths
  if #el.colspecs == 6 then
    widths = {0.13, 0.18, 0.16, 0.13, 0.14, 0.26}
  elseif #el.colspecs == 4 then
    local first = pandoc.utils.stringify(el.head.rows[1].cells[1].contents)
    if first:match('Source Identifier') then
      widths = {0.18, 0.22, 0.14, 0.46}
    else
      widths = {0.23, 0.18, 0.39, 0.20}
    end
  end
  if widths then
    for i, width in ipairs(widths) do el.colspecs[i][2] = width end
  end
  return {pandoc.RawBlock('latex', '\\begingroup\\small'), el, pandoc.RawBlock('latex', '\\endgroup')}
end


-- These solutions fit on one page. Treat them as indivisible print blocks
-- rather than estimating their height from the number of math expressions.
local compact_solutions = {
  ['[MAT223 Handout Page 2, Question 5]'] = true,
  ['[Textbook Section 13.3, Exercise 5]'] = true,
  ['[Textbook Section 13.4, Exercise 13]'] = true,
  ['[Textbook Section 13.4, Exercise 45]'] = true,
  ['[Textbook Section 13.4, Exercise 49]'] = true,
}

local function keep_compact_solutions(blocks)
  local result = pandoc.List()
  local inside = false
  for _, block in ipairs(blocks) do
    if inside == 'question' and block.t == 'Para' and block.content[1]
      and block.content[1].t == 'Strong'
      and pandoc.utils.stringify(block.content[1]):match('^Relevant method:') then
      result:insert(pandoc.RawBlock('latex', '\\end{minipage}\\par'))
      inside = false
    end
    if block.t == 'Header' then
      if inside then
        result:insert(pandoc.RawBlock('latex', '\\end{minipage}\\par'))
        inside = false
      end
      if compact_solutions[pandoc.utils.stringify(block.content)] then
        result:insert(pandoc.RawBlock('latex', '\\par\\noindent\\begin{minipage}{\\linewidth}'))
        inside = 'solution'
      elseif pandoc.utils.stringify(block.content):match('^%[') then
        -- A source heading, citation, and question must start together.
        result:insert(pandoc.RawBlock('latex', '\\par\\noindent\\begin{minipage}{\\linewidth}'))
        inside = 'question'
      end
    end
    result:insert(block)
  end
  if inside then result:insert(pandoc.RawBlock('latex', '\\end{minipage}\\par')) end
  return result
end

return {
  {Blocks = keep_compact_solutions},
  {Header = Header, Para = Para, Image = Image, Code = Code, HorizontalRule = HorizontalRule,
   Link = Link, Table = Table},
}
