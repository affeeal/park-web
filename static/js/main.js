function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(".question-vote").on('click', function (e) {
  e.preventDefault();
  
  const id = $(this).data('id')
  const vote = $(this).data('vote')
  
  const request = new Request(
    'http://0.0.0.0:8000/question_vote/',
    {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: 'question_id=' + id + '&question_vote=' + vote,
    },
  );

  fetch(request).then(
    response_raw => response_raw.json().then(
      response_json => {
        $("#question-rating-" + id).html(response_json.rating);
        $(this).prop('checked', !$(this).prop('checked'));
      }
    )
  );
});

$(".answer-vote").on('click', function (e) {
  e.preventDefault();
  
  const id = $(this).data('id')
  const vote = $(this).data('vote')
  
  const request = new Request(
    'http://0.0.0.0:8000/answer_vote/',
    {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: 'answer_id=' + id + '&answer_vote=' + vote,
    },
  );

  fetch(request).then(
    response_raw => response_raw.json().then(
      response_json => {
        $("#answer-rating-" + id).html(response_json.rating);
        $(this).prop('checked', !$(this).prop('checked'));
      }
    )
  );
});
