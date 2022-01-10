import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http:HttpClient) { }

  function10(_identificator_nr:string, _role:string){
    const options = {
      headers:{
        "Ocp-Apim-Subscription-Key": environment.OCIM_APIM_SUBSCRIPTION_KEY
      },
      params: {
        identificator_nr:_identificator_nr,
        role:_role
      }
    }
    return this.http.get(environment.API_HOST + "Function10", options)
  }

  function11(){
    const options = {
      headers:{
        "Ocp-Apim-Subscription-Key": environment.OCIM_APIM_SUBSCRIPTION_KEY
      }
    }
    return this.http.get(environment.API_HOST + "Function11", options)
  }

  function3(_identificator_nr:string, _date:string, _lesson:any){
    const options = {
      headers:{
        "Ocp-Apim-Subscription-Key": environment.OCIM_APIM_SUBSCRIPTION_KEY
      },
      params: {
        identificator_nr:_identificator_nr,
        date:_date,
        lesson: _lesson
      }
    }
    return this.http.get(environment.API_HOST + "Function3", options)
  }

  function12(_identificator_nr?:string,_role?:string,_lesson_id?:number, _justification?:string, _package?:{id?:number, name?:string}){
    const options = {
      headers:{
        "Ocp-Apim-Subscription-Key": environment.OCIM_APIM_SUBSCRIPTION_KEY
      },
      "responseType": 'text' as 'text'
    }
    const body = {
      identificator_nr: _identificator_nr,
      role: _role,
      package: {
        package_id: _package?.id,
        package_name: _package?.name
      },
      lesson_type_id: _lesson_id,
      justification: _justification
    }
    return this.http.post(environment.API_HOST + "Function12", body, options)
  }

}
