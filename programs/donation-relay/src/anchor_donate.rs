use anchor_spl::{associated_token::AssociatedToken,token_interface::{Mint,TokenAccount,TokenInterface}};
include!("state/v1/epoch_tracker.rs");
include!("state/v1/debouncer.rs");
include!("instructions/v1/public_api/donate/donate.rs");
include!("instructions/v1/public_api/donate/donate_pubkey_config_id.rs");
include!("instructions/v1/public_api/donate/donate_pubkey_config_id_with_payer.rs");
#[derive(AnchorSerialize,AnchorDeserialize,Clone)]
pub enum DaasEventDiscriminator {DonationV1,DonationEpochClosedV1,DonationEpochProcessedV1,DonationEpochJustSwappedV1}
#[event]
pub struct DonationMadeV1Event {
 pub daas_event_discriminator:DaasEventDiscriminator,pub config_id:[u8;32],pub mint:Pubkey,pub epoch:u128,
 pub gross_amount:u64,pub tip:u64,pub message:String,pub credited_to:Pubkey,
}
fn donation_error(code:crate::business_error_codes::ErrorCode,origin:Option<(&'static str,u32)>)->anchor_lang::error::Error {
 anchor_lang::error::AnchorError {error_name:code.name(),error_code_number:code.into(),error_msg:code.to_string(),
 error_origin:origin.map(|(filename,line)|anchor_lang::error::ErrorOrigin::Source(anchor_lang::error::Source{filename,line})),compared_values:None}.into()
}
fn donation_body(ctx:&mut Context<DonateV1>,amount:u64,config_id:[u8;32],tip_bps:u16,message:String,credited_to:Pubkey)->Result<DonationMadeV1Event> {
 use crate::business_error_codes::ErrorCode as Code;
 if message.len()>=256 {return Err(donation_error(Code::InvalidMessageLength,Some(("programs/contracts/src/tools/checks.rs",55))));}
 if tip_bps>10000 {return Err(donation_error(Code::InvalidBps,Some(("programs/contracts/src/tools/checks.rs",192))));}
 let owner=*ctx.accounts.mint.to_account_info().owner;
 if owner.to_bytes()!=crate::codec::constants::TOKEN && owner.to_bytes()!=crate::codec::constants::TOKEN2022 {return Err(donation_error(Code::InvalidTokenProgram,None));}
 let mint=ctx.accounts.mint.key();
 if mint.to_bytes()!=crate::codec::constants::NATIVE && mint.to_bytes()!=crate::codec::constants::NATIVE2022 && !ctx.accounts.mint_whitelist.mints.contains(&mint) {
  let info=ctx.accounts.mint.to_account_info();let data=info.data.borrow();
  let safe=crate::mint_policy::safe_mint_data(&data,owner.to_bytes()==crate::codec::constants::TOKEN2022).map_err(|e|match e {crate::mint_policy::DecodeError::InvalidAccountData=>ProgramError::InvalidAccountData,crate::mint_policy::DecodeError::UninitializedAccount=>ProgramError::UninitializedAccount})?;
  if !safe {return Err(donation_error(Code::MintNotSafeForDonation,Some(("programs/contracts/src/tools/checks.rs",184))));}
 }
 let tracker=&mut ctx.accounts.epoch_tracker;
 if tracker.state==EpochTrackerV1State::Uninitialized {
  tracker.bump=ctx.bumps.epoch_tracker;tracker.state=EpochTrackerV1State::Initialized;tracker.config_id=config_id;tracker.mint=mint;tracker.current_epoch=0;
 }
 let debouncer=&mut ctx.accounts.debouncer;
 if debouncer.state==DebouncerV1State::Uninitialized {
  debouncer.bump=ctx.bumps.debouncer;debouncer.state=DebouncerV1State::Initialized;debouncer.config_id=config_id;debouncer.mint=mint;debouncer.total_amount=0;
 }
 let shared="programs/contracts/src/tools/donate/shared.rs";
 if tracker.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,102))));}
 if debouncer.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,110))));}
 if debouncer.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,118))).with_pubkeys((debouncer.mint,mint)));}
 if debouncer.state!=DebouncerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,123))));}
 if tracker.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,127))).with_pubkeys((tracker.mint,mint)));}
 if tracker.state!=EpochTrackerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,132))));}
 let before=ctx.accounts.debouncer_token_account.amount;
 anchor_spl::token_interface::transfer_checked(CpiContext::new(ctx.accounts.token_program.to_account_info(),anchor_spl::token_interface::TransferChecked {
  from:ctx.accounts.from_token_account.to_account_info(),mint:ctx.accounts.mint.to_account_info(),to:ctx.accounts.debouncer_token_account.to_account_info(),authority:ctx.accounts.from.to_account_info(),
 }),amount,ctx.accounts.mint.decimals)?;
 ctx.accounts.debouncer_token_account.reload()?;
 let delta=ctx.accounts.debouncer_token_account.amount.checked_sub(before).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 let product=delta.checked_mul(u64::from(tip_bps)).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 debouncer.total_amount=debouncer.total_amount.checked_add(delta).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 Ok(DonationMadeV1Event{daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id,mint,epoch:tracker.current_epoch,gross_amount:delta,tip:product/10000,message,credited_to})
}

fn donation_body_pubkey(ctx:&mut Context<DonatePubkeyConfigIdV1>,amount:u64,config_id:[u8;32],tip_bps:u16,message:String,credited_to:Pubkey)->Result<DonationMadeV1Event> {
 use crate::business_error_codes::ErrorCode as Code;
 if message.len()>=256 {return Err(donation_error(Code::InvalidMessageLength,Some(("programs/contracts/src/tools/checks.rs",55))));}
 if tip_bps>10000 {return Err(donation_error(Code::InvalidBps,Some(("programs/contracts/src/tools/checks.rs",192))));}
 let owner=*ctx.accounts.mint.to_account_info().owner;
 if owner.to_bytes()!=crate::codec::constants::TOKEN && owner.to_bytes()!=crate::codec::constants::TOKEN2022 {return Err(donation_error(Code::InvalidTokenProgram,None));}
 let mint=ctx.accounts.mint.key();
 if mint.to_bytes()!=crate::codec::constants::NATIVE && mint.to_bytes()!=crate::codec::constants::NATIVE2022 && !ctx.accounts.mint_whitelist.mints.contains(&mint) {
  let info=ctx.accounts.mint.to_account_info();let data=info.data.borrow();
  let safe=crate::mint_policy::safe_mint_data(&data,owner.to_bytes()==crate::codec::constants::TOKEN2022).map_err(|e|match e {crate::mint_policy::DecodeError::InvalidAccountData=>ProgramError::InvalidAccountData,crate::mint_policy::DecodeError::UninitializedAccount=>ProgramError::UninitializedAccount})?;
  if !safe {return Err(donation_error(Code::MintNotSafeForDonation,Some(("programs/contracts/src/tools/checks.rs",184))));}
 }
 let tracker=&mut ctx.accounts.epoch_tracker;
 if tracker.state==EpochTrackerV1State::Uninitialized {
  tracker.bump=ctx.bumps.epoch_tracker;tracker.state=EpochTrackerV1State::Initialized;tracker.config_id=config_id;tracker.mint=mint;tracker.current_epoch=0;
 }
 let debouncer=&mut ctx.accounts.debouncer;
 if debouncer.state==DebouncerV1State::Uninitialized {
  debouncer.bump=ctx.bumps.debouncer;debouncer.state=DebouncerV1State::Initialized;debouncer.config_id=config_id;debouncer.mint=mint;debouncer.total_amount=0;
 }
 let shared="programs/contracts/src/tools/donate/shared.rs";
 if tracker.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,102))));}
 if debouncer.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,110))));}
 if debouncer.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,118))).with_pubkeys((debouncer.mint,mint)));}
 if debouncer.state!=DebouncerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,123))));}
 if tracker.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,127))).with_pubkeys((tracker.mint,mint)));}
 if tracker.state!=EpochTrackerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,132))));}
 let before=ctx.accounts.debouncer_token_account.amount;
 anchor_spl::token_interface::transfer_checked(CpiContext::new(ctx.accounts.token_program.to_account_info(),anchor_spl::token_interface::TransferChecked {
  from:ctx.accounts.from_token_account.to_account_info(),mint:ctx.accounts.mint.to_account_info(),to:ctx.accounts.debouncer_token_account.to_account_info(),authority:ctx.accounts.from.to_account_info(),
 }),amount,ctx.accounts.mint.decimals)?;
 ctx.accounts.debouncer_token_account.reload()?;
 let delta=ctx.accounts.debouncer_token_account.amount.checked_sub(before).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 let product=delta.checked_mul(u64::from(tip_bps)).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 debouncer.total_amount=debouncer.total_amount.checked_add(delta).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 Ok(DonationMadeV1Event{daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id,mint,epoch:tracker.current_epoch,gross_amount:delta,tip:product/10000,message,credited_to})
}

fn donation_body_payer(ctx:&mut Context<DonatePubkeyConfigIdWithPayerV1>,amount:u64,config_id:[u8;32],tip_bps:u16,message:String,credited_to:Pubkey)->Result<DonationMadeV1Event> {
 use crate::business_error_codes::ErrorCode as Code;
 if message.len()>=256 {return Err(donation_error(Code::InvalidMessageLength,Some(("programs/contracts/src/tools/checks.rs",55))));}
 if tip_bps>10000 {return Err(donation_error(Code::InvalidBps,Some(("programs/contracts/src/tools/checks.rs",192))));}
 let owner=*ctx.accounts.mint.to_account_info().owner;
 if owner.to_bytes()!=crate::codec::constants::TOKEN && owner.to_bytes()!=crate::codec::constants::TOKEN2022 {return Err(donation_error(Code::InvalidTokenProgram,None));}
 let mint=ctx.accounts.mint.key();
 if mint.to_bytes()!=crate::codec::constants::NATIVE && mint.to_bytes()!=crate::codec::constants::NATIVE2022 && !ctx.accounts.mint_whitelist.mints.contains(&mint) {
  let info=ctx.accounts.mint.to_account_info();let data=info.data.borrow();
  let safe=crate::mint_policy::safe_mint_data(&data,owner.to_bytes()==crate::codec::constants::TOKEN2022).map_err(|e|match e {crate::mint_policy::DecodeError::InvalidAccountData=>ProgramError::InvalidAccountData,crate::mint_policy::DecodeError::UninitializedAccount=>ProgramError::UninitializedAccount})?;
  if !safe {return Err(donation_error(Code::MintNotSafeForDonation,Some(("programs/contracts/src/tools/checks.rs",184))));}
 }
 let tracker=&mut ctx.accounts.epoch_tracker;
 if tracker.state==EpochTrackerV1State::Uninitialized {
  tracker.bump=ctx.bumps.epoch_tracker;tracker.state=EpochTrackerV1State::Initialized;tracker.config_id=config_id;tracker.mint=mint;tracker.current_epoch=0;
 }
 let debouncer=&mut ctx.accounts.debouncer;
 if debouncer.state==DebouncerV1State::Uninitialized {
  debouncer.bump=ctx.bumps.debouncer;debouncer.state=DebouncerV1State::Initialized;debouncer.config_id=config_id;debouncer.mint=mint;debouncer.total_amount=0;
 }
 let shared="programs/contracts/src/tools/donate/shared.rs";
 if tracker.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,102))));}
 if debouncer.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,110))));}
 if debouncer.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,118))).with_pubkeys((debouncer.mint,mint)));}
 if debouncer.state!=DebouncerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,123))));}
 if tracker.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,127))).with_pubkeys((tracker.mint,mint)));}
 if tracker.state!=EpochTrackerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,132))));}
 let before=ctx.accounts.debouncer_token_account.amount;
 anchor_spl::token_interface::transfer_checked(CpiContext::new(ctx.accounts.token_program.to_account_info(),anchor_spl::token_interface::TransferChecked {
  from:ctx.accounts.from_token_account.to_account_info(),mint:ctx.accounts.mint.to_account_info(),to:ctx.accounts.debouncer_token_account.to_account_info(),authority:ctx.accounts.from.to_account_info(),
 }),amount,ctx.accounts.mint.decimals)?;
 ctx.accounts.debouncer_token_account.reload()?;
 let delta=ctx.accounts.debouncer_token_account.amount.checked_sub(before).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 let product=delta.checked_mul(u64::from(tip_bps)).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 debouncer.total_amount=debouncer.total_amount.checked_add(delta).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 Ok(DonationMadeV1Event{daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id,mint,epoch:tracker.current_epoch,gross_amount:delta,tip:product/10000,message,credited_to})
}

fn donation_body_native(ctx:&mut Context<DonateNativeV1>,amount:u64,config_id:[u8;32],tip_bps:u16,message:String,credited_to:Pubkey)->Result<DonationMadeV1Event> {
 use crate::business_error_codes::ErrorCode as Code;
 if message.len()>=256 {return Err(donation_error(Code::InvalidMessageLength,Some(("programs/contracts/src/tools/checks.rs",55))));}
 if tip_bps>10000 {return Err(donation_error(Code::InvalidBps,Some(("programs/contracts/src/tools/checks.rs",192))));}
 let owner=*ctx.accounts.mint.to_account_info().owner;
 if owner.to_bytes()!=crate::codec::constants::TOKEN && owner.to_bytes()!=crate::codec::constants::TOKEN2022 {return Err(donation_error(Code::InvalidTokenProgram,None));}
 let mint=ctx.accounts.mint.key();
 if mint.to_bytes()!=crate::codec::constants::NATIVE && mint.to_bytes()!=crate::codec::constants::NATIVE2022 && !ctx.accounts.mint_whitelist.mints.contains(&mint) {
  let info=ctx.accounts.mint.to_account_info();let data=info.data.borrow();
  let safe=crate::mint_policy::safe_mint_data(&data,owner.to_bytes()==crate::codec::constants::TOKEN2022).map_err(|e|match e {crate::mint_policy::DecodeError::InvalidAccountData=>ProgramError::InvalidAccountData,crate::mint_policy::DecodeError::UninitializedAccount=>ProgramError::UninitializedAccount})?;
  if !safe {return Err(donation_error(Code::MintNotSafeForDonation,Some(("programs/contracts/src/tools/checks.rs",184))));}
 }
 let tracker=&mut ctx.accounts.epoch_tracker;
 if tracker.state==EpochTrackerV1State::Uninitialized {
  tracker.bump=ctx.bumps.epoch_tracker;tracker.state=EpochTrackerV1State::Initialized;tracker.config_id=config_id;tracker.mint=mint;tracker.current_epoch=0;
 }
 let debouncer=&mut ctx.accounts.debouncer;
 if debouncer.state==DebouncerV1State::Uninitialized {
  debouncer.bump=ctx.bumps.debouncer;debouncer.state=DebouncerV1State::Initialized;debouncer.config_id=config_id;debouncer.mint=mint;debouncer.total_amount=0;
 }
 let shared="programs/contracts/src/tools/donate/shared.rs";
 if tracker.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,102))));}
 if debouncer.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,110))));}
 if debouncer.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,118))).with_pubkeys((debouncer.mint,mint)));}
 if debouncer.state!=DebouncerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,123))));}
 if tracker.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,127))).with_pubkeys((tracker.mint,mint)));}
 if tracker.state!=EpochTrackerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,132))));}
 let before=ctx.accounts.debouncer_token_account.amount;
 anchor_spl::token_interface::transfer_checked(CpiContext::new(ctx.accounts.token_program.to_account_info(),anchor_spl::token_interface::TransferChecked {
  from:ctx.accounts.temp_wsol_token_account.to_account_info(),mint:ctx.accounts.mint.to_account_info(),to:ctx.accounts.debouncer_token_account.to_account_info(),authority:ctx.accounts.from.to_account_info(),
 }),amount,ctx.accounts.mint.decimals)?;
 ctx.accounts.debouncer_token_account.reload()?;
 let delta=ctx.accounts.debouncer_token_account.amount.checked_sub(before).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 let product=delta.checked_mul(u64::from(tip_bps)).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 debouncer.total_amount=debouncer.total_amount.checked_add(delta).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 Ok(DonationMadeV1Event{daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id,mint,epoch:tracker.current_epoch,gross_amount:delta,tip:product/10000,message,credited_to})
}

fn donation_body_native_pubkey(ctx:&mut Context<DonateNativePubkeyConfigIdV1>,amount:u64,config_id:[u8;32],tip_bps:u16,message:String,credited_to:Pubkey)->Result<DonationMadeV1Event> {
 use crate::business_error_codes::ErrorCode as Code;
 if message.len()>=256 {return Err(donation_error(Code::InvalidMessageLength,Some(("programs/contracts/src/tools/checks.rs",55))));}
 if tip_bps>10000 {return Err(donation_error(Code::InvalidBps,Some(("programs/contracts/src/tools/checks.rs",192))));}
 let owner=*ctx.accounts.mint.to_account_info().owner;
 if owner.to_bytes()!=crate::codec::constants::TOKEN && owner.to_bytes()!=crate::codec::constants::TOKEN2022 {return Err(donation_error(Code::InvalidTokenProgram,None));}
 let mint=ctx.accounts.mint.key();
 if mint.to_bytes()!=crate::codec::constants::NATIVE && mint.to_bytes()!=crate::codec::constants::NATIVE2022 && !ctx.accounts.mint_whitelist.mints.contains(&mint) {
  let info=ctx.accounts.mint.to_account_info();let data=info.data.borrow();
  let safe=crate::mint_policy::safe_mint_data(&data,owner.to_bytes()==crate::codec::constants::TOKEN2022).map_err(|e|match e {crate::mint_policy::DecodeError::InvalidAccountData=>ProgramError::InvalidAccountData,crate::mint_policy::DecodeError::UninitializedAccount=>ProgramError::UninitializedAccount})?;
  if !safe {return Err(donation_error(Code::MintNotSafeForDonation,Some(("programs/contracts/src/tools/checks.rs",184))));}
 }
 let tracker=&mut ctx.accounts.epoch_tracker;
 if tracker.state==EpochTrackerV1State::Uninitialized {
  tracker.bump=ctx.bumps.epoch_tracker;tracker.state=EpochTrackerV1State::Initialized;tracker.config_id=config_id;tracker.mint=mint;tracker.current_epoch=0;
 }
 let debouncer=&mut ctx.accounts.debouncer;
 if debouncer.state==DebouncerV1State::Uninitialized {
  debouncer.bump=ctx.bumps.debouncer;debouncer.state=DebouncerV1State::Initialized;debouncer.config_id=config_id;debouncer.mint=mint;debouncer.total_amount=0;
 }
 let shared="programs/contracts/src/tools/donate/shared.rs";
 if tracker.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,102))));}
 if debouncer.config_id!=config_id {return Err(donation_error(Code::InvalidConfigId,Some((shared,110))));}
 if debouncer.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,118))).with_pubkeys((debouncer.mint,mint)));}
 if debouncer.state!=DebouncerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,123))));}
 if tracker.mint!=mint {return Err(donation_error(Code::InvalidMint,Some((shared,127))).with_pubkeys((tracker.mint,mint)));}
 if tracker.state!=EpochTrackerV1State::Initialized {return Err(donation_error(Code::InvalidState,Some((shared,132))));}
 let before=ctx.accounts.debouncer_token_account.amount;
 anchor_spl::token_interface::transfer_checked(CpiContext::new(ctx.accounts.token_program.to_account_info(),anchor_spl::token_interface::TransferChecked {
  from:ctx.accounts.temp_wsol_token_account.to_account_info(),mint:ctx.accounts.mint.to_account_info(),to:ctx.accounts.debouncer_token_account.to_account_info(),authority:ctx.accounts.from.to_account_info(),
 }),amount,ctx.accounts.mint.decimals)?;
 ctx.accounts.debouncer_token_account.reload()?;
 let delta=ctx.accounts.debouncer_token_account.amount.checked_sub(before).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 let product=delta.checked_mul(u64::from(tip_bps)).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 debouncer.total_amount=debouncer.total_amount.checked_add(delta).ok_or_else(||donation_error(Code::ArithmeticOverflow,None))?;
 Ok(DonationMadeV1Event{daas_event_discriminator:DaasEventDiscriminator::DonationV1,config_id,mint,epoch:tracker.current_epoch,gross_amount:delta,tip:product/10000,message,credited_to})
}

fn native_program_supported(program:&Pubkey)->bool {
 program.to_bytes()==crate::codec::constants::TOKEN || program.to_bytes()==crate::codec::constants::TOKEN2022
}
fn native_mint_for_program(program:&Pubkey)->Result<Pubkey> {
 if program.to_bytes()==crate::codec::constants::TOKEN {Ok(Pubkey::new_from_array(crate::codec::constants::NATIVE))}
 else if program.to_bytes()==crate::codec::constants::TOKEN2022 {Ok(Pubkey::new_from_array(crate::codec::constants::NATIVE2022))}
 else {Err(crate::business_error_codes::ErrorCode::InvalidTokenProgram.into())}
}
fn native_mint_pair(mint:&Pubkey,program:&Pubkey)->bool {
 native_mint_for_program(program).map(|expected|expected==*mint).unwrap_or_default()
}
include!("instructions/v1/public_api/donate/donate_native.rs");
include!("instructions/v1/public_api/donate/donate_native_pubkey_config_id.rs");
