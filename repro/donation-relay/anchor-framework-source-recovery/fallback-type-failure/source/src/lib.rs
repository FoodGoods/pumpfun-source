//! Combined source trial: authentic Anchor reserved framework plus recovered business paths.
use anchor_lang::prelude::*;
declare_id!("RLAYHr9TRFcKB2ubYQhspcnXiaGpaVzNQvHytt47RZu");
#[program]
pub mod relay_anchor_idl_reconstruction_probe {
    use super::*;
    pub fn fallback<'info>(program_id: &Pubkey, accounts: &[AccountInfo<'info>], data: &[u8]) -> anchor_lang::solana_program::entrypoint::ProgramResult {
        legacy::entrypoint::process_instruction(program_id, accounts, data)
    }
}
