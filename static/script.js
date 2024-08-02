
async function translateText() {
  const inputText = document.getElementById('hinglishInput').value;
  if (!inputText) {
      alert('Please enter text to translate.');
      return;
  }

  try {
      const response = await fetch('/translate', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
      }

      const data = await response.json();
      document.getElementById('translationResult').innerText = data.translation;
  } catch (error) {
      console.error('Error:', error);
      document.getElementById('translationResult').innerText = 'An error occurred: ' + error.message;
  }
}

