
(()=>{

  function createCodeTableLine(lineNum, line) {
    return `<tr><td>${lineNum}</td><td>${line}</td></tr>`
  }
  function createCodeTable(srcCode) {
    let lines = srcCode.split(/\r?\n/)   
    let lineNum = 0 
    lines = lines.map(line =>createCodeTableLine(++lineNum, line))
    const tableContent = lines.join("\n") 
    return `<table class="code">
${tableContent}
</table>`
  }

  async function attachCode(src, element) {
    const res = await fetch(src)

    if (res.ok) {
      const codeStr = await res.text()
      const codeTable = createCodeTable(codeStr)
      element.innerHTML = codeTable
    }
  }

  window.eghttp = {
    attachCode
  }

})()


// vi: se ts=2 sw=2 et:
