import EmailServerController from "./Server/EmailServerController";
import DictStorage from "./Storage/DictStorage";
import RestServerController from "./Server/RestServerController";


let storage = new DictStorage();
storage.setup();

const email_controller = new EmailServerController({name: "emailtester.test"}, storage);
const rest_controller = new RestServerController(storage);


rest_controller.init();
email_controller.init()