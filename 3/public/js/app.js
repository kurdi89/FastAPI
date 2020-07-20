console.log('Hello Udacians')
function getCookie (cname) {
  var name = cname + '='
  var decodedCookie = decodeURIComponent(document.cookie)
  var ca = decodedCookie.split(';')
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i]
    while (c.charAt(0) == ' ') {
      c = c.substring(1)
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length)
    }
  }
  return ''
}

var APP_process = getCookie('APP_process')
var APP_original_image = getCookie('APP_original_image')
var APP_style = getCookie('APP_style')

console.log({ APP_process })

function fetch_interval () {
  img_3 = document.getElementById('3')
  fetch('/export/' + APP_process + '.jpg', { method: 'HEAD' })
    .then(res => {
      if (res.ok) {
        console.log('Image exists.')
        img_3.src = '/export/' + APP_process + '.jpg'
        /* later */
        clearInterval(refreshIntervalId)
      } else {
        console.log('Image does not exist.')
      }
    })
    .catch(err => console.log('Error:', err))
}

if (APP_process != '') {
  img_1 = document.getElementById('1')
  img_1.src = '/upload/' + APP_original_image
  img_2 = document.getElementById('2')
  img_2.src = '/public/img/' + APP_style + '.jpg'
  var refreshIntervalId = setInterval(fetch_interval, 1000)
} else {
  // do nothing
}
