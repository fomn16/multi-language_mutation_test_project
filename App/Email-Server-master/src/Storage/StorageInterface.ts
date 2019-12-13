export interface StorageObject{
  id?:number, subject: string, to:string, from:string, body: string
}

export interface SearchableObject{
  id?:number, subject?:string, to?:string, from?:string
}

export default abstract class StorageInterface{

  /**
   * Setup your database
   */
  public abstract setup():void;

/**   * 
   * @param toStore Object to store in database
   * @returns Número inteiro positivo do id do objeto no storage. Caso haja problemas em salva-lo, retorna -1
   */
  public abstract async store(toStore:StorageObject):Promise<number>;

  /**
   * @returns List of objects matching search params
   */
  public abstract async search(toSearch:SearchableObject):Promise<StorageObject[]>;

  /**
   * Delete all stored objects
   */
  public abstract async reset():Promise<boolean>;

  /**
   * Return all objects stored
   */
  public abstract async all():Promise<StorageObject[]>;
}