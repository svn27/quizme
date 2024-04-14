fetch('http://127.0.0.1:5000/getanswers/MXJ-zpJeY3E/10/hard')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Log the fetched data to the console
    console.log(data);
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });