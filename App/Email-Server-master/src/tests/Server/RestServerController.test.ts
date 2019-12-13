import RestServerController from "../../Server/RestServerController"
import { StorageObject } from "../../Storage/StorageInterface";
import axios from 'axios'

let server:RestServerController;
let validObject:StorageObject;

describe('RestServerController', ()=>{

  beforeEach(()=>{
    server =  new RestServerController();
    server.storage.setup();
    validObject = {
      to: "Receiver",
      from: "Sencer",
      subject: "Test case",
      body: "This is my test case"
    }
  })

  describe("Initialization works", ()=>{
    it('Creates server and initialize it', ()=>{
      expect(()=>{
        server.init(()=>{})
        server.close()
      }).not.toThrow()
    })

  })

  describe("Routes", ()=>{
    
    it('#Index /emails', async ()=>{
      server.init(()=>{});
      await server.storage.store(validObject);

      let response =  await axios.get(`http://localhost:${server.port}/emails`)

      expect(response.data["emails"].length).toBe(1);
      server.server.close();
    })

    describe("Search", ()=>{
      it('Return correct content searched', async ()=>{
        server.init(()=>{});
        await server.storage.store(validObject);

        let response =  await axios.get(`http://localhost:${server.port}/emails/search?id=1`)
        let received = response.data["emails"][0]
  
        expect(received.body).toBe(validObject.body);
        server.server.close();
      })

      it('Return nothing when searching invalid', async ()=>{
        server.init(()=>{});
        await server.storage.store(validObject);

        let response =  await axios.get(`http://localhost:${server.port}/emails/search?id=4`)
        let received = response.data["emails"]
  
        expect(received.length).toBe(0);
        server.server.close();
      })

    })
  })

})