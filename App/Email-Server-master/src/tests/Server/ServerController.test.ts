
import EmailServerController from '../../Server/EmailServerController';
import { Server } from 'net';
import { execShellCommand } from '../../utils/helpers';

describe('ServerController', () => {

  describe("Creating server", ()=>{
    test('it should create server', ()=>{
      const server = new EmailServerController();
    
      expect(server.init()).toBeInstanceOf(Server);
      server.close();
    })
    
    test('it should change server options', ()=>{
      const server = new EmailServerController({
        name: "test133"
      });
  
      expect(server.server.options.name).toBe("test133")
    })
  })

  test('receives messsage', async ()=>{
    const server = new EmailServerController();
    server.storage.setup();
    server.init(()=>{})
    
    let messages = await server.storage.all();
    let oldLentgh = messages.length;
    await execShellCommand('./scripts/test.sh');
    
    messages = await server.storage.all();
    expect(messages.length).toBeGreaterThan(oldLentgh);
    server.close();
  }, 1200000);


})
