
(()=>{


  async function fetchText(textPath) {
    const res = await fetch(textPath)
    let result = null
    if (res.ok) {
      result = await res.text()
    }
    return result
  }

  async function renderDiagrams() {

    const diagramTargets = [
      [
        'load-template-before.mermaid',
        'load-template-before',
      ],
      [
        'load-template-after.mermaid',
        'load-template-after'
      ],
      [
        'template-location.mermaid',
        'template-location'
      ]
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

  async function renderMarkdown() {
    const mdTargets = [
      ['refactor-design.md', 'design']
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


  function toggleImg(selectedElement) {
    const imgs = document.querySelectorAll('img[data-refactor]')
    imgs.forEach(item => {
      if (item.dataset.refactor == selectedElement.value) {
        item.style.display = "block"
      } else {
        item.style.display = "none"
      }
    })
  }
  function toggleDiagrams(selectedElement) {
    const diagrams = document.querySelectorAll('div[data-refactor]')
    diagrams.forEach(item => {
      if (item.dataset.refactor == selectedElement.value) {
        item.style.display = "block"
      } else {
        item.style.display = "none"
      }
    })
  }


  function attachRadio(elem) {
    elem.addEventListener('change', (event)=>{
      if (event.target.checked) {
        toggleImg(event.target)
        toggleDiagrams(event.target)
      }
    }) 
  }

  async function loaded(e) {
    const radios = document.querySelectorAll('.refactor-1 input[type="radio"]')
    radios.forEach(attachRadio)

    await renderDiagrams()
    await renderMarkdown()
  }

  window.addEventListener('load', loaded)

})()


// vi: se ts=2 sw=2 et:
