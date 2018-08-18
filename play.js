/**
* 設定
*/
const googlehome = require('google-home-notifier');
const msg = process.argv[2] || 'なんか喋ってよ'; // process.argv[2]で引数を取得。ない場合はデフォルトメッセージを代入


/**
* 喋らせる関数
*/
function say(text, language = 'ja'){
  googlehome.device('Google-Home', language);
  googlehome.notify(text, function(res) {
    console.log(res);
  });
}

say(msg);