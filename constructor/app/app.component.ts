import { Component } from '@angular/core';
// import { DinosaurService } from './services/dinosaurService'

@Component({
  selector: 'constructor-app',
  template: `<h1>Дима - {{name}}</h1>`
  // providers: [DinosaurService]
})

export class AppComponent {
  name:string = 'Жопа'
}
