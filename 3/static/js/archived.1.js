$.post('/', {
  category: category, // <---- This is the info payload you send to the server.
    }).done(function(data){ // <!--- This is a callback that is being called after the server finished with the request.
      // Here you dynamically change parts of your content, in this case we modify the construction-projects container.
    $('#construction-projects').html(data.result.map(item => `
      <div class="col-md-4">
      <div class="card card-plain card-blog">
        <div class="card-body">
        <h6 class="card-category text-info">${category}</h6>
        <h4 class="card-title">
          <a href="#pablo">${item.title_intro.substring(0, 40)}...</a>
          </h4>
          <p class="card-description">
          ${item.description_intro.substring(0, 80)}... <br>
            <a href="#pablo"> Read More </a>
            </p>
          </div>
      </div>
    </div>
  `))
    
  }).fail(function(){
    console.log('error') // <!---- This is the callback being called if there are Internal Server problems.
    });