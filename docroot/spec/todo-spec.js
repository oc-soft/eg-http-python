
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
      ['todo-spec.md', 'spec']
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
        'todo-spec/get-todo.mermaid',
        'get-todo',
      ],
      [
        'todo-spec/post-todo.mermaid',
        'post-todo',
      ],
      [
        'todo-spec/get-todo-flow.mermaid',
        'get-todo-flow',
      ],
      [
        'todo-spec/post-todo-flow.mermaid',
        'post-todo-flow',
      ],
      [
        'todo-spec/todo-html-loc.mermaid',
        'todo-html-loc',
      ],
      [
        'todo-spec/todo-css-loc.mermaid',
        'todo-css-loc',
      ],
      [
        'todo-spec/todo-txt-loc.mermaid',
        'todo-txt-loc',
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
