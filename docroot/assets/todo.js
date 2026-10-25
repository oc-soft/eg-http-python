
(() => {
  /**
   * TODOリストを更新
   */
  function updateTodoElement(
    targetElem,
    todoList) {
    // TODOリストを包含する要素の全ての子要素を削除
    targetElem.replaceChildren() 
    // <ul>要素を作成
    const ulElem = document.createElement("ul")
    // TODOリストを包含する要素に<ul>を追加
    targetElem.append(ulElem)
    
    // todo項目を1つずつ取り出して、リスト要素に追加する
    for (item of todoList) {
      // チェックボックス
      const inputElem = document.createElement("input")
      inputElem.setAttribute("type", "checkbox") 
      inputElem.setAttribute("name", "done")
      inputElem.value = item
      // ラベル
      const labelElem = document.createElement("label")
      // チェックボックスを追加
      labelElem.append(inputElem)
      // 項目を追加
      labelElem.append(item)
      // リスト要素<li>
      const liElem = document.createElement("li")
      // ラベルを<li>に追加
      liElem.append(labelElem)
      // <ul>に<li>を追加
      ulElem.append(liElem)
    }
  }

  /**
   * TODOリストUIを更新
   */
  function updateTodoList(todoList) {
    // TODOリストを包含する要素を取得
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
    // evtを発行した要素は、form要素
    const formData = new FormData(evt.target)  
    // リクエストのbodyを作成するためのオブジェクト
    const searchParams = new URLSearchParams()
    for (const [key, value] of formData.entries()) {
      searchParams.append(key, value)
    } 
    const headers = new Headers()
    // ヘッダにjson書式での応答を要求していることを設定
    headers.append('Accept', 'application/json')
    // サーバにtodoリストを要求
    const res = await fetch('/todo', {
      headers,
      method: 'POST',
      body: searchParams.toString() 
    })
    if (res.ok) {
      // 正常応答の場合、応答結果のjsonでブラウザのTODOリストを更新
      updateTodoList(await res.json())
      // 送信で使用された入力データをクリア
      clearElementValue(evt.target)
    }
  }
  /**
   * htmlページ要素が全てロードされた時に呼び出される
   */
  async function ready() {
    const headers = new Headers()
    // ヘッダにjson書式での応答を要求していることを設定
    headers.append('Accept', 'application/json')
    // サーバにTODOリストを要求
    const res = await fetch('/todo', {
      headers 
    })
    if (res.ok) {
      // 正常応答の場合、応答結果のjsonでブラウザのTODOリストを更新
      updateTodoList(await res.json())
    }

    // form要素を取得
    const formElem = document.querySelector('form[action="todo"]') 
    // form要素で、submitイベントが発行された場合の処理を追加
    formElem.addEventListener('submit', handleNewItemAction) 
  }
  // 全ての要素がロードされた時の処理を追加
  window.addEventListener('load', ready)
})()

// vi: se ts=2 sw=2 et:
