import express from 'express'
import StorageInterface from '../Storage/StorageInterface';
import url  from 'url';
import DictStorage from '../Storage/DictStorage';
import { Server } from 'http';


export default class RestServerController{

  private app =  express()
  public port = 3001;
  public server:Server;
  constructor(public storage: StorageInterface = new DictStorage()){}

  init(logFun = console.log){
    this.setup();
    this.server = this.app.listen(this.port,()=>{
      logFun(`REST Server alive on port ${this.port}`)
    });
  }
  
  close(){
    this.server.close()
  }
  
  private createRoutes(){
    
    /** Index */
    this.app.get('/emails', async (req, res)=>{
      res.status(200).send({
        emails: await this.storage.all()
      }
      )
    })
    
    /** Search */
    this.app.get('/emails/search/', async (req, res)=>{
      res.status(200).send({
        emails: await this.storage.search(req.query)
      }
      )
    })
  }

  private setup(){
    this.createRoutes();
  }
}