import {firebase} from '../server/firebase';
// Run only with an explicitly approved uid and a server credential in the environment.
const [uid,mode]=process.argv.slice(2);
if(!uid||!['grant','revoke'].includes(mode)||!process.env.FIREBASE_PROJECT_ID)throw new Error('Usage: tsx --env-file=.env.local scripts/admin-access.ts APPROVED_UID grant|revoke');
const {auth,db}=firebase();const user=await auth.getUser(uid);if(!user.emailVerified)throw new Error('Verified Google account required');
await auth.setCustomUserClaims(uid,{...user.customClaims,admin:mode==='grant'});await auth.revokeRefreshTokens(uid);
await db.collection('audit').add({action:`admin.${mode}`,entityId:uid,actorId:'project-owner-cli',createdAt:new Date().toISOString()});console.log('Permission updated. User must sign in again.');
