//! Real Anchor reserved operations and the complete recovered business implementation.
use anchor_lang::prelude::*;
declare_id!("RLAYHr9TRFcKB2ubYQhspcnXiaGpaVzNQvHytt47RZu");
#[program]
pub mod relay_anchor_idl_reconstruction_probe {}
anchor_lang::solana_program::entrypoint!(process_instruction);
fn process_instruction<'info>(program_id: &Pubkey, accounts: &'info [AccountInfo<'info>], data: &[u8]) -> anchor_lang::solana_program::entrypoint::ProgramResult {
    let reserved = data.starts_with(&[64,244,188,120,167,233,105,10]) || data.starts_with(&[228,69,165,46,81,203,154,29]);
    if reserved || data.len() < 8 || *program_id != ID {
        entry(program_id, accounts, data)
    } else {
        legacy::entrypoint::process_instruction(program_id, accounts, data)
    }
}
