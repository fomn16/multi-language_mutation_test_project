import { generate_storage } from "./helpers/generators"




for(let i=0; i<process.argv.length; i+=1){
  let arg = process.argv[i]

  if(arg.startsWith('Storage')){
    generate_storage(process.argv[i+1])
    i+=1;
  }

}