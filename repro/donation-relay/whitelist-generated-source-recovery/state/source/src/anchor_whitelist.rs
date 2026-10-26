// Generated account structure recovered from parser156 and the captured IDL.
include!("state/v1/mint_whitelist.rs");
#[derive(Accounts)]
pub struct UpsertMintWhitelistV1<'info> {
    #[account(init_if_needed, payer=signer, space=1037, seeds=[b"mint_whitelist_v1".as_ref()], bump, rent_exempt=enforce)]
    pub mint_whitelist: Account<'info,MintWhitelistV1>,
    #[account(mut, address=Pubkey::new_from_array(crate::codec::constants::RELAYER))]
    pub signer: Signer<'info>,
    pub system_program: Program<'info,System>,
}
fn business_error(code:crate::business_error_codes::ErrorCode, filename:&'static str, line:u32) -> anchor_lang::error::Error {
    anchor_lang::error::AnchorError {
        error_name:code.name(), error_code_number:code.into(), error_msg:code.to_string(),
        error_origin:Some(anchor_lang::error::ErrorOrigin::Source(anchor_lang::error::Source{filename,line})),
        compared_values:None,
    }.into()
}
fn check_relayer(signer:&Signer<'_>) -> Result<()> {
    let key=signer.key();let expected=Pubkey::new_from_array(crate::codec::constants::RELAYER);
    if key!=expected {
        return Err(business_error(crate::business_error_codes::ErrorCode::SignerIsNotRelayer,
            "programs/contracts/src/tools/checks.rs",80).with_pubkeys((key,expected)));
    }
    Ok(())
}
fn upsert_whitelist(whitelist:&mut MintWhitelistV1,mints:Vec<Pubkey>,bump:u8)->Result<()> {
    if mints.len()>32 {return Err(business_error(crate::business_error_codes::ErrorCode::InvalidMintWhitelist,
        "programs/contracts/src/instructions/v1/relayer_only/upsert_mint_whitelist.rs",33));}
    whitelist.mints=mints;whitelist.bump=bump;Ok(())
}
