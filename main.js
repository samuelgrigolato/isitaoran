

function check(event) {

  var answer = document.getElementById('answer');
  var word = document.getElementById('word').value.trim();

  if (word) {
    var url = 'https://60b7stpn67.execute-api.us-east-1.amazonaws.com/default/aoran?word=' + word;
    fetch(url).then(
      function (resp) {
        if (resp.status === 200) {
          resp.json().then(
            function (json) {
              answer.innerText = json['article'] + ' ' + word;
            },
            function (err) {
              console.error(err);
              answer.innerText = 'Unable to process your request :(';
            }
          )
        } else if (resp.status === 404) {
          answer.innerText = 'Sorry, I couldn\'t find this word :(';
        }
      },
      function (err) {
        console.error(err);
        answer.innerText = 'Unable to process your request :(';
      }
    )
  }

}
