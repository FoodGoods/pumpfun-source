//! Typed instruction bodies; common amounts are converted to events before wrapper emission.
use anchor_lang::prelude::*;
use crate::anchor_framework::*;
pub fn donate_v1_handler(accounts:&mut DonateV1,args:crate::codec::wire::DonateV1,epoch_tracker_bump:u8,debouncer_bump:u8)->Result<DonationMadeV1Event> {

            let (epoch,gross_amount,tip)=crate::shared_donation::donate_shared(crate::shared_donation::DonationContext {
                epoch_tracker:&mut accounts.epoch_tracker,debouncer:&mut accounts.debouncer,from:&accounts.from,mint_whitelist:&accounts.mint_whitelist,
                debouncer_token_account:accounts.debouncer_token_account.to_account_info(),mint:accounts.mint.to_account_info(),from_token_account:accounts.from_token_account.to_account_info(),token_program:accounts.token_program.to_account_info(),
            },crate::shared_donation::DonationArgs {config_id:args.config_id,amount:args.amount,tip_bps:args.tip_bps,message:args.message.clone(),epoch_tracker_bump:epoch_tracker_bump,debouncer_bump:debouncer_bump})?;
            let event=DonationMadeV1Event {daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id:args.config_id,mint:accounts.mint.key(),epoch,gross_amount,tip,message:args.message,credited_to:args.credited_to};
            
            
            Ok(event)
        
}
pub fn donate_pubkey_config_id_v1_handler(accounts:&mut DonatePubkeyConfigIdV1,args:crate::codec::wire::DonatePubkeyConfigIdV1,epoch_tracker_bump:u8,debouncer_bump:u8)->Result<DonationMadeV1Event> {

            let (epoch,gross_amount,tip)=crate::shared_donation::donate_shared(crate::shared_donation::DonationContext {
                epoch_tracker:&mut accounts.epoch_tracker,debouncer:&mut accounts.debouncer,from:&accounts.from,mint_whitelist:&accounts.mint_whitelist,
                debouncer_token_account:accounts.debouncer_token_account.to_account_info(),mint:accounts.mint.to_account_info(),from_token_account:accounts.from_token_account.to_account_info(),token_program:accounts.token_program.to_account_info(),
            },crate::shared_donation::DonationArgs {config_id:args.config_id.to_bytes(),amount:args.amount,tip_bps:args.tip_bps,message:args.message.clone(),epoch_tracker_bump:epoch_tracker_bump,debouncer_bump:debouncer_bump})?;
            let event=DonationMadeV1Event {daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id:args.config_id.to_bytes(),mint:accounts.mint.key(),epoch,gross_amount,tip,message:args.message,credited_to:args.credited_to};
            
            
            Ok(event)
        
}
pub fn donate_pubkey_config_id_with_payer_v1_handler(accounts:&mut DonatePubkeyConfigIdWithPayerV1,args:crate::codec::wire::DonatePubkeyConfigIdWithPayerV1,epoch_tracker_bump:u8,debouncer_bump:u8)->Result<DonationMadeV1Event> {

            let (epoch,gross_amount,tip)=crate::shared_donation::donate_shared(crate::shared_donation::DonationContext {
                epoch_tracker:&mut accounts.epoch_tracker,debouncer:&mut accounts.debouncer,from:&accounts.from,mint_whitelist:&accounts.mint_whitelist,
                debouncer_token_account:accounts.debouncer_token_account.to_account_info(),mint:accounts.mint.to_account_info(),from_token_account:accounts.from_token_account.to_account_info(),token_program:accounts.token_program.to_account_info(),
            },crate::shared_donation::DonationArgs {config_id:args.config_id.to_bytes(),amount:args.amount,tip_bps:args.tip_bps,message:args.message.clone(),epoch_tracker_bump:epoch_tracker_bump,debouncer_bump:debouncer_bump})?;
            let event=DonationMadeV1Event {daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id:args.config_id.to_bytes(),mint:accounts.mint.key(),epoch,gross_amount,tip,message:args.message,credited_to:args.credited_to};
            
            
            Ok(event)
        
}
pub fn donate_native_v1_handler(accounts:&mut DonateNativeV1,args:crate::codec::wire::DonateNativeV1,epoch_tracker_bump:u8,debouncer_bump:u8)->Result<DonationMadeV1Event> {

            anchor_lang::system_program::transfer(CpiContext::new(accounts.system_program.to_account_info(),anchor_lang::system_program::Transfer {from:accounts.from.to_account_info(),to:accounts.temp_wsol_token_account.to_account_info()}),args.amount)?;
            anchor_spl::token_interface::sync_native(CpiContext::new(accounts.token_program.to_account_info(),anchor_spl::token_interface::SyncNative {account:accounts.temp_wsol_token_account.to_account_info()}))?;
            let (epoch,gross_amount,tip)=crate::shared_donation::donate_shared(crate::shared_donation::DonationContext {
                epoch_tracker:&mut accounts.epoch_tracker,debouncer:&mut accounts.debouncer,from:&accounts.from,mint_whitelist:&accounts.mint_whitelist,
                debouncer_token_account:accounts.debouncer_token_account.to_account_info(),mint:accounts.mint.to_account_info(),from_token_account:accounts.temp_wsol_token_account.to_account_info(),token_program:accounts.token_program.to_account_info(),
            },crate::shared_donation::DonationArgs {config_id:args.config_id,amount:args.amount,tip_bps:args.tip_bps,message:args.message.clone(),epoch_tracker_bump:epoch_tracker_bump,debouncer_bump:debouncer_bump})?;
            let event=DonationMadeV1Event {daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id:args.config_id,mint:accounts.mint.key(),epoch,gross_amount,tip,message:args.message,credited_to:args.credited_to};
            anchor_spl::token_interface::close_account(CpiContext::new(accounts.token_program.to_account_info(),anchor_spl::token_interface::CloseAccount {account:accounts.temp_wsol_token_account.to_account_info(),destination:accounts.from.to_account_info(),authority:accounts.from.to_account_info()}))?;
            Ok(event)
        
}
pub fn donate_native_pubkey_config_id_v1_handler(accounts:&mut DonateNativePubkeyConfigIdV1,args:crate::codec::wire::DonateNativePubkeyConfigIdV1,epoch_tracker_bump:u8,debouncer_bump:u8)->Result<DonationMadeV1Event> {

            anchor_lang::system_program::transfer(CpiContext::new(accounts.system_program.to_account_info(),anchor_lang::system_program::Transfer {from:accounts.from.to_account_info(),to:accounts.temp_wsol_token_account.to_account_info()}),args.amount)?;
            anchor_spl::token_interface::sync_native(CpiContext::new(accounts.token_program.to_account_info(),anchor_spl::token_interface::SyncNative {account:accounts.temp_wsol_token_account.to_account_info()}))?;
            let (epoch,gross_amount,tip)=crate::shared_donation::donate_shared(crate::shared_donation::DonationContext {
                epoch_tracker:&mut accounts.epoch_tracker,debouncer:&mut accounts.debouncer,from:&accounts.from,mint_whitelist:&accounts.mint_whitelist,
                debouncer_token_account:accounts.debouncer_token_account.to_account_info(),mint:accounts.mint.to_account_info(),from_token_account:accounts.temp_wsol_token_account.to_account_info(),token_program:accounts.token_program.to_account_info(),
            },crate::shared_donation::DonationArgs {config_id:args.config_id.to_bytes(),amount:args.amount,tip_bps:args.tip_bps,message:args.message.clone(),epoch_tracker_bump:epoch_tracker_bump,debouncer_bump:debouncer_bump})?;
            let event=DonationMadeV1Event {daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id:args.config_id.to_bytes(),mint:accounts.mint.key(),epoch,gross_amount,tip,message:args.message,credited_to:args.credited_to};
            anchor_spl::token_interface::close_account(CpiContext::new(accounts.token_program.to_account_info(),anchor_spl::token_interface::CloseAccount {account:accounts.temp_wsol_token_account.to_account_info(),destination:accounts.from.to_account_info(),authority:accounts.from.to_account_info()}))?;
            Ok(event)
        
}
