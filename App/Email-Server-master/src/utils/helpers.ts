import { exec } from 'child_process';
import { StorageObject } from '../Storage/StorageInterface';
/**
 * Executes a shell command and return it as a Promise.
 * @param cmd {string}
 * @return {Promise<string>}
 */
function execShellCommand(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.warn(error);
      }
      resolve(stdout? stdout : stderr);
    });
  });
}

/**
   * email format: 
   * 
   * @param emailStr {` Received: (from root@localhost)
   *    by thiago-Inspiron-7472 (8.15.2/8.15.2/Submit) id xAUMdLfQ005545;
   *    Sat, 30 Nov 2019 19:39:22 -0300
   *  Date: Sat, 30 Nov 2019 19:39:22 -0300
   *  From: root <root@thiago-Inspiron-7472>
   *  Message-Id: <201911302239.xAUMdLfQ005545@thiago-Inspiron-7472> 
   *  Subject: Testando email\n Testando 
   *  To: <localhost@suniaster> 
   *  X-Mailer: mail (GNU Mailutils 3.4)
   *  
   *  Teste email`}
  */
function parseEmailString(emailStr:string):StorageObject{
  let lines = emailStr.split("\n")
  let subject;
  let to;
  let from;
  let body = "";
  let bodyInic = false;
  lines.forEach((line)=>{
    if(line.startsWith("From")){
      let arr = line.split(" ")
      from = arr[arr.length - 1];
    }
    if(line.startsWith("To")){
      let arr = line.split(" ")
      to = arr[arr.length - 1];
    }
    if(line.startsWith("Subject")){
      subject = line.split("Subject: ")[1];
    }

    if(bodyInic) body+=line;
    if(!line.replace(/\s/g, '').length) bodyInic = true;
  })

  return {
    to:       removeFromString(to, ['\r', '\<', '\>']),
    from:     removeFromString(from, ['\r', '\<', '\>']),
    subject:  removeFromString(subject, ['\r']),
    body:     removeFromString(body, ['\r'])
  }
}

function removeFromString(str,toRemovelist:string[]):string{
  toRemovelist.forEach((rm)=>{
    str = str.replace(rm, '')
  })
  return str;
}

function extendObject(obj, src) {
  Object.keys(src).forEach(function(key) { obj[key] = src[key]; });
  return obj;
}

export { execShellCommand , parseEmailString, extendObject, removeFromString}