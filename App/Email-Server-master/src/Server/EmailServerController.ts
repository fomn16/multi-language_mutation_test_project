import {SMTPServer, SMTPServerOptions, SMTPServerDataStream, SMTPServerSession} from 'smtp-server'
import StorageInterface, { StorageObject } from '../Storage/StorageInterface';
import DictStorage from '../Storage/DictStorage';
import { parseEmailString, extendObject } from '../utils/helpers';
// const { PassThrough, Writable } = require('stream');


export default class EmailServerController{
  server : SMTPServer;
  name:string;
  PORT = 25;
  constructor(configs: SMTPServerOptions = {}, public storage:StorageInterface = new DictStorage()){
    //! To change later
    const options: SMTPServerOptions = {
      disabledCommands: ['STARTTLS', 'AUTH'],
      onData: this.handleMessage
    }
    
    this.name = configs.name == undefined ? "localhost" : configs.name
    this.server = new SMTPServer(extendObject(options, configs));
  }

  handleMessage = (stream:SMTPServerDataStream, session:SMTPServerSession, callback: (err?:Error)=> void) =>{
    let str = "";
    stream.on('data', (chunk) => { str+= chunk });

    stream.on('end', ()=>{
      this.storage.store(
        parseEmailString(str)
      )
      callback();
    })
  }


  init(logFun = console.log){
    return this.server.listen(this.PORT, ()=>{
      logFun(
        `Email:\tServer started, listening on port 25.\n\tSend Email to some_user@${this.name}`
        );
    });
  }

  close(callback = () =>{} ){
    this.server.close(callback);
  }

}

// sudo lsof -i -P -n | grep LISTEN
// sudo /etc/init.d/sendmail stop