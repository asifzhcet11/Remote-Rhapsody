import {Component, OnInit} from '@angular/core';
import {GoogleLoginProvider, SocialAuthService, SocialUser} from "angularx-social-login";
import {AuthorizationService} from "./authorization.service";
import {UserInformationService} from "../services/user-information.service";



@Component({
  selector: 'app-google-login',
  templateUrl: './google-login.component.html',
  styleUrls: ['./google-login.component.css']
})
export class GoogleLoginComponent implements OnInit {

  user: SocialUser;
  userName: string;
  profilePicture: string;
  email: string;
  loggedIn: boolean;
  syncCode: number;
  googleLoginOptions = {
    scope: 'email profile openid https://www.googleapis.com/auth/calendar',
    offline_access: true
  };


  constructor(private authenticationService: SocialAuthService,
              private authorizationService: AuthorizationService,
              private userInformationService: UserInformationService) { }

  ngOnInit(): void {

    this.authenticationService.authState.subscribe((user) => {
      this.user = user;
      this.loggedIn = (user != null);
      if (this.loggedIn){
        this.userInformationService.name = user.name;
        this.userName = user.name;
        this.profilePicture = user.photoUrl;
        this.email = user.email;
        this.userInformationService.email = user.email;

      }

      if(this.loggedIn){
        if (user.authorizationCode != undefined){
          this.authorizationService.saveAuthorizationCode({
            email: user.email,
            authorizationCode: user.authorizationCode,
            synchronizaionCode: this.syncCode
          }).subscribe(responseData => {
            this.userName = responseData.name;
            this.profilePicture = responseData.picture;
            this.email = responseData.email;
            this.userInformationService.email = responseData.email;
            this.userInformationService.name = responseData.name;
          });
        }
      }
    });
  }

  signIn(): void {
    this.authenticationService.signIn(GoogleLoginProvider.PROVIDER_ID, this.googleLoginOptions)
  }

  signOut(): void{
    this.authenticationService.signOut();
  }

}
