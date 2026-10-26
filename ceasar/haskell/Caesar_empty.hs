-- Chiffrement de César + déchiffrement par force brute.
module Main
  ( main
  ) where

import           Data.Char          (isDigit)
import           System.Environment (getArgs)
import           System.Exit        (ExitCode (..), exitWith)
import           System.IO

usage :: String
usage =
  unlines
    ["usage:", "  caesar encrypt <shift> <text>", "  caesar decrypt <text>"]

-- | Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions.
encrypt :: Integer -> String -> String
encrypt _shift _text = error "TODO: encrypt"

-- | Force brute : renvoie les 26 candidats, l'élément k étant le texte
-- déchiffré en supposant un décalage de k.
decrypt :: String -> [String]
decrypt _text = error "TODO: decrypt"

die :: String -> IO a
die msg = do
  hPutStrLn stderr ("error: " ++ msg)
  hPutStr stderr usage
  exitWith (ExitFailure 1)

parseShift :: String -> IO Integer
parseShift s =
  case s of
    ('-':ds)
      | valid ds -> pure (negate (read ds))
    ds
      | valid ds -> pure (read ds)
    _ -> die ("invalid shift '" ++ s ++ "'")
  where
    valid ds = not (null ds) && all isDigit ds

main :: IO ()
main = do
  hSetEncoding stdout utf8
  hSetEncoding stderr utf8
  args <- getArgs
  case args of
    ["encrypt", s, text] -> do
      shift <- parseShift s
      putStrLn (encrypt shift text)
    ["decrypt", text] ->
      mapM_
        (\(k, candidate) -> putStrLn (show k ++ ": " ++ candidate))
        (zip [0 :: Int ..] (decrypt text))
    [] -> die "missing command"
    (cmd:_)
      | cmd `elem` ["encrypt", "decrypt"] -> die "wrong number of arguments"
      | otherwise -> die ("unknown command '" ++ cmd ++ "'")
