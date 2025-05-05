async function fetchSummary(event) {
  event.preventDefault()

  const multipleUrls = document.getElementById('multipleUrlsInput').value.trim()

  let urls = []

  // Adicionar múltiplas URLs se fornecidas
  if (multipleUrls) {
    const urlLines = multipleUrls.split('\n').filter((url) => url.trim() !== '')
    urls = [...urls, ...urlLines]
  }

  if (urls.length === 0) {
    showError('Por favor, insira pelo menos uma URL válida.')
    return
  }

  // Mostrar loading e esconder mensagens de erro
  document.getElementById('loading').style.display = 'block'
  document.getElementById('errorMessage').style.display = 'none'
  document.getElementById('resultsContainer').innerHTML = ''

  try {
    const response = await fetch('http://127.0.0.1:8000/get-by-urls', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-API-Key': 'abc@123',
      },
      body: JSON.stringify({
        urls: urls,
      }),
    })

    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.status}`)
    }

    const data = await response.json()
    console.log('🚀 ~ fetchSummary ~ data:', data)
    displayResults(data)
  } catch (error) {
    console.log(error)
    showError(`Falha ao processar a requisição: ${error.message}`)
  } finally {
    console.log('finally')
    document.getElementById('loading').style.display = 'none'
  }
}

function displayResults(data) {
  const resultsContainer = document.getElementById('resultsContainer')
  resultsContainer.innerHTML = ''

  if (data.error) {
    showError(data.error)
    return
  }

  // Exibir mensagem de sucesso
  const messageElement = document.createElement('p')
  messageElement.textContent = data.message
  resultsContainer.appendChild(messageElement)

  // Exibir resultados
  if (data.results && data.results.length > 0) {
    data.results.forEach((result) => {
      const resultCard = document.createElement('div')
      resultCard.className = 'result-card'

      // Título
      const titleElement = document.createElement('div')
      titleElement.className = 'result-title'
      titleElement.textContent = result.title || 'Sem título'
      resultCard.appendChild(titleElement)

      // URL
      const urlElement = document.createElement('a')
      urlElement.className = 'result-url'
      urlElement.textContent = result.url
      urlElement.href = result.url
      urlElement.target = '_blank'
      resultCard.appendChild(urlElement)

      // Conteúdo original
      const contentSection = document.createElement('div')
      contentSection.className = 'result-section'

      const contentLabel = document.createElement('div')
      contentLabel.className = 'result-label'
      contentLabel.textContent = 'Conteúdo Original:'
      contentSection.appendChild(contentLabel)

      const contentText = document.createElement('div')
      contentText.textContent = result.content || 'Sem conteúdo'
      contentSection.appendChild(contentText)

      resultCard.appendChild(contentSection)

      // Resumo
      const summarySection = document.createElement('div')
      summarySection.className = 'result-section'

      const summaryLabel = document.createElement('div')
      summaryLabel.className = 'result-label'
      summaryLabel.textContent = 'Resumo:'
      summarySection.appendChild(summaryLabel)

      const summaryText = document.createElement('div')
      summaryText.textContent =
        result.resume_summarized || 'Sem resumo disponível'
      summarySection.appendChild(summaryText)

      resultCard.appendChild(summarySection)

      resultsContainer.appendChild(resultCard)
    })
  } else {
    const noResultsElement = document.createElement('p')
    noResultsElement.textContent = 'Nenhum resultado encontrado.'
    resultsContainer.appendChild(noResultsElement)
  }
}

function showError(message) {
  const errorElement = document.getElementById('errorMessage')
  errorElement.textContent = message
  errorElement.style.display = 'block'
}
