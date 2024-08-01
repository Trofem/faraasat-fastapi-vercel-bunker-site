document.getElementById("generateCharacterButton").addEventListener("click", generateCharacter);

function generateCharacter() {
  fetch("/api/character")
    .then(response => response.json())
    .then(data => {
      // Display the generated character on the page
      document.getElementById("characterContainer").innerHTML = `
        <h2>Generated Character</h2>
        <p>Name: ${data.name}</p>
        <p>Age: ${data.age}</p>
        <p>Occupation: ${data.occupation}</p>
      `;
    })
    .catch(error => {
      console.error("Error:", error);
    });
}