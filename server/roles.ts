// Project owner explicitly designated this account. This policy runs only
// after Firebase Admin has verified the token, including revocation checks.
const administratorEmail='frankmercadopeerez@gmail.com';
export function isAdministrator(token:{admin?:unknown;email?:string;email_verified?:boolean;firebase?:{sign_in_provider?:string}}){
 return token.admin===true||(token.email_verified===true&&token.firebase?.sign_in_provider==='google.com'&&token.email?.toLowerCase()===administratorEmail);
}
