(()=>{
  async function fetchText(path) {
    let result = null
    const res = await fetch(path)
    if (res.ok) {
      result = res.text()
    }
    return result
  }
  async function renderMarkdown() {
    const mdTargets = [
      ['ui-js-1.md', 'spec']
    ]
    for (const mdTarget of mdTargets) {
     
      const txt = await fetchText(mdTarget[0])
      if (txt) {
        const elem = document.querySelector(`#${mdTarget[1]}`)
        if (elem) {
          elem.innerHTML = marked.parse(txt)
        }
      }
    }
  }
  async function renderDiagrams() {

    const diagramTargets = [
      [
        'ui-js-1/post-todo-1.mermaid',
        'post-todo-1',
      ],
      [
        'ui-js-1/post-todo-2.mermaid',
        'post-todo-2',
      ],
      [
        'ui-js-1/render-html-srv-flow-1.mermaid',
        'render-html-srv-flow-1',
      ],
      [
        'ui-js-1/render-html-js-seq-1.mermaid',
        'render-html-js-seq-1',
      ],
      [
        'ui-js-1/render-html-js-flow-1.mermaid',
        'render-html-js-flow-1',
      ],
    ]
    for (const diagramTarget of diagramTargets) {
     
      const tmp = await fetchText(diagramTarget[0])
      if (tmp) {
        const elem = document.querySelector(`#${diagramTarget[1]}`)
        if (elem) {
          const {svg} = await mermaid.render(`mermaid-${diagramTarget[1]}`, tmp)  
          elem.innerHTML = svg
        }
      }
    }
 
  } 
  async function loaded(e) {
    await renderMarkdown()
    await renderDiagrams()
  }
  window.addEventListener('load', loaded)
})()
// vi: se ts=2 sw=2 et:
