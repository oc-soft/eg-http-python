
(() => {
  /**
   * TODOリストを更新
   */
  function updateTodoElement(
    targetElem,
    todoList) {
    // 全ての子要素を削除
    targetElem.replaceChildren() 
    const ulElem = document.createElement("ul")
    targetElem.append(ulElem)
    
    for (item of todoList) {
      const inputElem = document.createElement("input")
      inputElem.setAttribute("type", "checkbox") 
      inputElem.setAttribute("name", "done")
      inputElem.value = item
      const labelElem = document.createElement("label")
      labelElem.append(inputElem)
      labelElem.append(item)
      const liElem = document.createElement("li")
      liElem.append(labelElem)
      ulElem.append(liElem)
    }
  }

  /**
   * todoリストUIを更新
   */
  function updateTodoList(todoList) {
    const todoItems = document.querySelector(".todo-items")  
    updateTodoElement(todoItems, todoList)
  }

  /**
   * formの入力を消去する
   */
  function clearElementValue(formElem) {
    for (const elem of formElem.elements) {
      if ('INPUT' === elem.nodeName && elem.type === 'text') {
        elem.value = ''
      }
    }
  }


  /**
   * 新規TODOのイベントに応答
   */
  async function handleNewItemAction(evt) {
    evt.preventDefault() 
    const formData = new FormData(evt.target)  
    const searchParams = new URLSearchParams()
    for (const [key, value] of formData.entries()) {
      searchParams.append(key, value)
    } 
    const headers = new Headers()
    headers.append('Content-Type', 'application/json')
    const res = await fetch('/todo', {
      headers,
      method: 'POST',
      body: searchParams.toString() 
    })
    if (res.ok) {
      updateTodoList(await res.json())
      clearElementValue(evt.target)
    }
  }
  /**
   * htmlページ要素が全てロードされた時に呼び出される
   */
  async function ready() {
    const headers = new Headers()
    headers.append('Content-Type', 'application/json')
    const res = await fetch('/todo', {
      headers 
    })
    if (res.ok) {
      updateTodoList(await res.json())
    }

    const formElem = document.querySelector('form[action="todo"]') 
    formElem.addEventListener('submit', handleNewItemAction) 
  }
  window.addEventListener('load', ready)
})()

// vi: se ts=2 sw=2 et:
