"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require("@angular/core");
var router_1 = require("@angular/router");
var home_page_component_1 = require("./home-page/home-page.component");
var courses_ts_1 = require("./Courses/courses.ts");
var AppComponent = (function () {
    function AppComponent() {
        this.name = 'ЛОЛ';
    }
    return AppComponent;
}());
AppComponent = __decorate([
    core_1.Component({
        selector: 'constructor-app',
        template: "\n  <a [routerLink]=\"['HomePage']\">\u0413\u043B\u0430\u0432\u043D\u0430\u044F</a>\n  <a [routerLink]=\"['/Courses']\">\u041A\u0443\u0440\u0441\u044B</a>\n  <router-outlet></router-outlet>\n  ",
        directives: [router_1.ROUTER_DIRECTIVES],
        providers: [router_1.ROUTER_PROVIDERS]
    }),
    router_1.RouteConfig([
        {
            path: '/',
            name: 'HomePage',
            component: home_page_component_1.HomePageComponent,
            useAsDefault: true
        },
        {
            path: '/courses',
            name: 'Courses',
            component: courses_ts_1.CoursesComponent
        }
    ]),
    __metadata("design:paramtypes", [])
], AppComponent);
exports.AppComponent = AppComponent;
//# sourceMappingURL=app.component.js.map