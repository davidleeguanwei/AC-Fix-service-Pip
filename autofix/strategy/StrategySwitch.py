import autofix.strategy.SwitchPythonStrategy
import autofix.strategy.FindSourceCodeStrategy
import autofix.strategy.syntax.AddColonWithClassStrategy
import autofix.strategy.syntax.AddParenthesesStrategy
import autofix.strategy.syntax.RemoveLInIntegerStrategy
import autofix.strategy.syntax.ReplaceAsyncWithAsyncnStrategy
import autofix.strategy.syntax.ReplaceAsyncWithGetAttrStrategy
import autofix.strategy.syntax.ReplaceCommaWithAsInExceptStrategy
import autofix.strategy.syntax.ReplaceCommaWithBracketsInRaiseStrategy
import autofix.strategy.syntax.ReplaceUrWithRInRegexStrategy
import autofix.strategy.syntax.Replace0With0oStrategy
import autofix.strategy.syntax.PutFromFutureAtFirstLineStrategy
import autofix.strategy.HandleAttributeErrorStrategy
from autofix.util.Singleton import Singleton

class StrategySwitch(metaclass=Singleton):
    def __init__(self):
        self._strategyMap = {
            'switch_python_version': getattr(autofix.strategy.SwitchPythonStrategy, 'switchPythonVersion'),
            'find_source_code': getattr(autofix.strategy.FindSourceCodeStrategy, 'findSourceCode'),
            'add_colon_with_class': getattr(autofix.strategy.syntax.AddColonWithClassStrategy, 'addColonWithClass'),
            'replace_async_with_asyncn': getattr(autofix.strategy.syntax.ReplaceAsyncWithAsyncnStrategy, 'replaceAsyncWithAsyncn'),
            'replace_async_with_getattr': getattr(autofix.strategy.syntax.ReplaceAsyncWithGetAttrStrategy, 'replaceAsyncWithGetAttr'),
            'replace_comma_with_as_in_except': getattr(autofix.strategy.syntax.ReplaceCommaWithAsInExceptStrategy, 'replaceCommaWithAsInExcept'),
            'replace_ur_with_r_in_regex': getattr(autofix.strategy.syntax.ReplaceUrWithRInRegexStrategy, 'replaceUrWithRInRegex'),
            'replace_0_with_0o': getattr(autofix.strategy.syntax.Replace0With0oStrategy, 'replace0With0o'),
            'replace_comma_with_brackets_in_raise': getattr(autofix.strategy.syntax.ReplaceCommaWithBracketsInRaiseStrategy, 'replaceCommaWithBracketsInRaise'),
            'add_parentheses': getattr(autofix.strategy.syntax.AddParenthesesStrategy, 'addParentheses'),
            'remove_L_in_int': getattr(autofix.strategy.syntax.RemoveLInIntegerStrategy, 'removeLInInteger'),
            'put_from_future_at_first_line': getattr(autofix.strategy.syntax.PutFromFutureAtFirstLineStrategy, 'putFromFutureAtFirstLine'),
            'handle_attribute_error': getattr(autofix.strategy.HandleAttributeErrorStrategy, 'handleAttributeError')
        }

    def getStrategy(self, key: str):
        if key == 'cannot_be_fixed':
            return None
        elif key not in self._strategyMap:
            return None
        return self._strategyMap[key]


if __name__ == '__main__':
    exit()
