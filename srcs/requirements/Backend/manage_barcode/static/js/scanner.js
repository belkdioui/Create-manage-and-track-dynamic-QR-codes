

  
let html5QrcodeScanner ;

function onScanSuccess(decodedText, decodedResult) {
	
	let video_container = document.getElementById('reader__scan_region').querySelector('video')
	console.log(`status = ${html5QrcodeScanner.getState()}`)
	if (html5QrcodeScanner.getState() == 2)
	{
		html5QrcodeScanner.pause()
		video_container.pause()
	}

	const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    console.log(`Code matched = ${decodedText}`);
    fetch('/qr_scanner/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ 'qr_code_data': decodedText })
    })
    .then(response => response.json())
    .then(data => {
      console.log(`this is data = ${data['success']}`)
      if (data['success'] == 'Ticket used')
      {
        createToast('success', 'Your ticket has been consumed');
		    setTimeout(() => {
			  html5QrcodeScanner.resume();
			  video_container.play();
		    }, 1000);
      }
      else
        createToast('error', data['error']);
      
		console.log(data)

    })
    .catch(error => {
      // Handle errors
      console.log(`error ${error}`)
  
    });
  
  }
  
  function onScanFailure(error) {
    // handle scan failure, usually better to ignore and keep scanning.
    // for example:
    // console.warn(`Code scan error = ${error}`);
  }

  html5QrcodeScanner= new Html5QrcodeScanner("reader", { fps: 60},  false);

html5QrcodeScanner.render(onScanSuccess, onScanFailure);
