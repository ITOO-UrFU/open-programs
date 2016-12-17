import { Component } from '@angular/core';
import { RouteConfig, ROUTER_DIRECTIVES, ROUTER_PROVIDERS} from "@angular/router";
import {HomePageComponent} from "./home-page/home-page.component"
import {CoursesComponent} from "./Courses/courses.ts";


@Component({
  selector: 'constructor-app',
  template: `
  <a [routerLink]="['HomePage']">Главная</a>
  <a [routerLink]="['/Courses']">Курсы</a>
  <router-outlet></router-outlet>
  `,
  directives: [ROUTER_DIRECTIVES],
  providers: [ROUTER_PROVIDERS]
})

@RouteConfig([
    {
        path: '/',
        name: 'HomePage',
        component: HomePageComponent,
        useAsDefault: true
    },

    {
        path: '/courses',
        name: 'Courses',
        component: CoursesComponent
    }

])

export class AppComponent {
  name:string = 'ЛОЛ'
}
