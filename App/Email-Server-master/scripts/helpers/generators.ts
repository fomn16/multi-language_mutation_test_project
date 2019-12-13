import { readFileSync, writeFile } from "fs";
import ejs from 'ejs'

function generate_storage(storage_name:string){
  let template_path = './scripts/templates/storage/';

  let storage_template = readFileSync(template_path+'new_storage.ejs', 'utf8');
  let test_template = readFileSync(template_path+'test.ejs', 'utf8');

  let newStorageFile = ejs.render(storage_template, {classname: storage_name});
  let test_file = ejs.render(test_template, {classname: storage_name});

  writeFile(`./src/Storage/${storage_name}.ts`, newStorageFile, ()=>{});
  writeFile(`./src/tests/Storage/${storage_name}.test.ts`, test_file, ()=>{});

  console.log("Created 2 files at:");
  console.log(`\t./src/Storage/${storage_name}.ts`)
  console.log(`\t./src/tests/Storage/${storage_name}.test.ts`)
}


export {generate_storage}