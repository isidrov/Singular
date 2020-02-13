const xapi = require('xapi');

const MYSPEED_DIAL_NUMBER = '+14089061916@cisco.com';

xapi.event.on('UserInterface Extensions Page Action', (event) => {
    if(event.Type == 'Opened' && event.PageId == 'help_desk'){
         xapi.command("dial", {Number: MYSPEED_DIAL_NUMBER});
    }
});